#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_set>

// Function to preprocess the dictionary
std::unordered_map<std::string, std::vector<std::string>> 
preprocessDictionary( const std::vector<std::pair<std::string, 
                                        std::string>>& dictionary ) 
{
    std::unordered_map<std::string, std::vector<std::string>> phonemeMap;
    for ( const auto& i : dictionary )
        phonemeMap[i.second].push_back( i.first );
    return ( phonemeMap );
}

// Function to join a vector of strings into a single string with a separator
std::string join( const std::vector<std::string>& vec, const std::string& sep ) 
{
    std::ostringstream result;
    for ( size_t i = 0; i < vec.size(); ++i ) 
    {
        result << vec[i];
        if ( i < vec.size() - 1 )
            result << sep;
    }
    return ( result.str() );
}

// Recursive function to find all combinations
void findCombinations( 
    const std::unordered_map<std::string, std::vector<std::string>>& phonemeMap, 
    const std::vector<std::string>& phonemes, 
    int index,     
    std::vector<std::string>& current,
    std::vector<std::vector<std::string>>& result )
{
    if ( index == phonemes.size() ) 
    {
        result.push_back( current );
        return;
    }

    for ( int len = 1; len <= phonemes.size() - index; ++len ) 
    {
        std::string subseq = join( 
                std::vector<std::string>( phonemes.begin() + index, 
                                          phonemes.begin() + index + len ), 
                " " );
        if ( phonemeMap.find( subseq ) != phonemeMap.end() ) 
        {
            for ( const auto& word : phonemeMap.at( subseq ) ) 
            {
                current.push_back( word );
                findCombinations( phonemeMap, 
                                  phonemes, 
                                  index + len, 
                                  current, 
                                  result );
                current.pop_back();
            }
        }
    }
}

int main() 
{
    // Dict
    std::vector<std::pair<std::string, std::string>> dictionary = {
        {"ABACUS", "AE B AH K AH S"},
        {"BOOK", "B UH K"},
        {"THEIR", "DH EH R"},
        {"THERE", "DH EH R"},
        {"TOMATO", "T AH M AA T OW"},
        {"TOMATO", "T AH M EY T OW"}
    };

    // Test
    std::vector<std::string> phonemes = {"DH", "EH", "R", "DH", "EH", "R"};

    // Preprocess the dictionary
    auto phonemeMap = preprocessDictionary( dictionary );

    // Find all combinations
    std::vector<std::vector<std::string>> result;
    std::vector<std::string> current;
    findCombinations( phonemeMap, phonemes, 0, current, result );

    // Print
    for ( const auto& combination : result )
    {
        for ( const auto& word : combination )
            std::cout << word << " ";
        std::cout << std::endl;
    }

    return 0;
}
