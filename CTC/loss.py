import torch
import numpy as np
import math


from utils import *

class CustomCTCLoss(torch.autograd.Function):
    @staticmethod
    def forward(ctx, matrix, gt, chars, epsilon=1e-10):
        # Convert mat to numpy array for processing
        mat_np = matrix.detach().cpu().numpy()

        # Compute probability using the provided functions
        prob = probability(mat_np, gt, chars)
        
        # Handle zero probability by adding a small epsilon
        prob = max(prob, epsilon)
        
        # Save for backward pass
        ctx.save_for_backward(matrix)
        ctx.gt = gt
        ctx.chars = chars
        ctx.prob = prob

        # Return negative log probability as the loss
        loss = -math.log(prob)

        return torch.tensor(loss, dtype=mat.dtype, device=mat.device)

    @staticmethod
    def backward(ctx, grad_output):
        matrix, = ctx.saved_tensors
        gt = ctx.gt
        chars = ctx.chars
        prob = ctx.prob

        # Convert mat to numpy for gradient calculation
        mat_np = matrix.detach().cpu().numpy()

        max_T, _ = mat_np.shape
        blank = len(chars)  # Index for the blank label
        labeling_with_blanks = extend_by_blanks(word_to_label_seq(gt, chars), blank)
        
        # Initialize forward and backward variables
        alpha = empty_cache(max_T, labeling_with_blanks)
        beta = empty_cache(max_T, labeling_with_blanks)

        # Calculate forward probabilities (alpha)
        for t in range(max_T - 1, -1, -1):
            for s in range(len(labeling_with_blanks) - 1, -1, -1):
                _ = recursive_forward_probability(t, s, mat_np, labeling_with_blanks, blank, alpha)
                if any_list_has_none(alpha) == False:
                    break


        # Calculate backward probabilities (beta)
        for t in range(max_T):
            for s in range(len(labeling_with_blanks)):
                _ = recursive_backward_probability(t, s, mat_np, labeling_with_blanks, blank, beta)
                if any_list_has_none(beta) == False:
                    break
        
        # Calculate the gradient
        grad_mat = np.zeros_like(mat_np)

        for t in range(max_T):
            for s in range(len(labeling_with_blanks)):
                grad_mat[t, labeling_with_blanks[s]] -= (alpha[t][s] * beta[t][s]) / prob

        # Convert numpy gradient to tensor and scale with grad_output
        grad_mat_tensor = torch.tensor(grad_mat, dtype=mat.dtype, device=mat.device)
        return grad_mat_tensor * grad_output, None, None

if __name__ == '__main__':
    chars = "abcdef,"
    gt = "cab"
    mat = torch.tensor(
        np.random.rand(2 * len(gt) + 1, len(chars) + 1),
        dtype=torch.float32,
        requires_grad=True)

    # Use custom CTC loss function
    loss_function = CustomCTCLoss.apply
    loss = loss_function(mat, gt, chars)
    print("loss value: ", loss.item())

    # Compute gradients
    loss.backward()
    print("---------------")
    print("gradient of the loss:\n",mat.grad)  # Gradient of the loss with respect to mat
