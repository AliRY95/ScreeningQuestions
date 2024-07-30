#include <iostream>
#include <vector>
#include <algorithm>

// Function to calculate the probability of having more than n rainy days in a 
// year
double probabilityOfMoreThanNRainyDays( const std::vector<double>& p, 
                                        int n ) 
{
    // Number of days
    int numDays = p.size();
    // If we are asking for too much or too less days, it is simple:
    if ( n > numDays )
        return ( 0. );
    else if ( n <= 0 )
        return ( 1. );
    
    // We solve it using dynamic programming. A 2D grid dp[i][j] with size 
    // (numDays + 1)x(numDays + 1) is created to track the probabilty of raining 
    // exactly j days in the first i days. Obviosuly, if j > i, the probability 
    // is zero.
    std::vector<std::vector<double>> dp( numDays + 1, 
                std::vector<double>    ( numDays + 1, 0. ) );
    
    // Base case
    dp[0][0] = 1.;

    // Populate the grid
    for ( int i = 1; i <= numDays; ++i ) 
    {
        for ( int j = 0; j <= i; ++j ) 
        {
            // It does not rain on the i-th day
            dp[i][j] = dp[i-1][j] * ( 1. - p[i-1] );
            // It rains on the i-th day
            dp[i][j] += dp[i-1][j-1] * p[i-1]; 
        }
    }

    // Calculate the probability of having more than n rainy days.
    // We start from n + 1, because everything before that is just zero.
    double result = 0.;
    for ( int j = n + 1; j <= numDays; ++j )
        result += dp[numDays][j];

    return ( result );
}

int main() 
{
    // Test
    std::vector<double> p( 365, 0.99 ); 
    int n = 364;
    double result = probabilityOfMoreThanNRainyDays( p, n );
    std::cout << "Probability of raining more than " 
              << n 
              << " days: " 
              << result 
              << std::endl;
    return 0;
}