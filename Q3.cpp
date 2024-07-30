#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <string>
#include <algorithm>
#include <cctype>

// Function to return an array of words given the path
std::vector<std::string> readFileAsWords( const std::string& filePath )
{
    // Read the file
    std::ifstream file( filePath );
    if ( !file.is_open() )
        throw std::runtime_error( "File not found!" );
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::istringstream stream( buffer.str() );

    // Create an array of words, all lowercase and removing punctutations
    std::vector<std::string> words;
    std::string word;
    while ( stream >> word )
    {
        // Remove punctuation from the word
        word.erase( std::remove_if( word.begin(), word.end(), ::ispunct ), 
                    word.end() );
        // Convert word to lowercase
        std::transform( word.begin(), word.end(), word.begin(), ::tolower );
        words.push_back( word );
    }
    return ( words );
}

// Function to count the frequency of each word. It can be combined with the
// last function, but this way it is much more cleaner.
std::unordered_map<std::string, int> 
countWords( const std::vector<std::string>& words ) 
{
    std::unordered_map<std::string, int> frequencyMap;
    for ( const auto& word : words )
        ++frequencyMap[word];
    return ( frequencyMap );
}

// Function to find the n most frequent words using a min-heap
std::vector<std::pair<std::string, int>> 
find_frequent_words( const std::string& filePath, int n ) 
{
    // Read the file
    std::vector<std::string> words = readFileAsWords( filePath );
    // Count the frequency of each word
    std::unordered_map<std::string, int> frequency = countWords( words );
    
    // Min-heap to keep track of the top n most frequent words
    auto comp = []( const std::pair<std::string, int>& a, 
                    const std::pair<std::string, int>& b )
                    { return a.second > b.second; };
    // Priority queue to keep the most frequent words
    std::priority_queue<std::pair<std::string, int>, 
                        std::vector<std::pair<std::string, int>>, 
                        decltype(comp)> minHeap(comp);

    for ( const auto& i : frequency )
    {
        minHeap.push( i );
        if ( minHeap.size() > n )
            minHeap.pop();
    }

    // Extract the most frequent words
    std::vector<std::pair<std::string, int>> mostFrequentWords;
    while ( !minHeap.empty() )
    {
        mostFrequentWords.push_back( minHeap.top() );
        minHeap.pop();
    }

    // Reverse the vector to get the words in descending order of frequency
    std::reverse( mostFrequentWords.begin(), mostFrequentWords.end() );
    return ( mostFrequentWords );
}

int main() 
{
    // Test
    std::string filePath = "./shakespeare.txt";
    int n = 15;
    std::vector<std::pair<std::string, int>> mostFrequentWords = 
                                    find_frequent_words( filePath, n );
    std::cout << "The " << n << " most frequent words are:\n";
    for ( const auto& pair : mostFrequentWords )
        std::cout << pair.first << ": " << pair.second << "\n";
    
    return 0;
}
