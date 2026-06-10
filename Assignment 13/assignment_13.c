#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// 1. Create the StringBuffer struct
typedef struct {
    char *data;      // Pointer to the actual string on the heap
    size_t length;   // Current number of characters (excluding null-terminator)
    size_t capacity; // Total allocated memory for the string
} StringBuffer;

// 2. Initialize the buffer safely
StringBuffer* sb_init(size_t initial_capacity) {
    // Allocate memory for the struct itself
    StringBuffer *sb = (StringBuffer*)malloc(sizeof(StringBuffer));
    if (sb == NULL) {
        return NULL; // Struct allocation failed
    }
    
    // Allocate memory for the internal string array
    sb->data = (char*)malloc(initial_capacity * sizeof(char));
    if (sb->data == NULL) {
        free(sb); // Prevent memory leak if data allocation fails
        return NULL; 
    }
    
    // Set initial state
    sb->data[0] = '\0'; 
    sb->length = 0;
    sb->capacity = initial_capacity;
    
    return sb;
}

// 3 & 4. Append text and handle safe reallocation
bool sb_append(StringBuffer *sb, const char *str) {
    if (sb == NULL || str == NULL) return false;
    
    size_t str_len = strlen(str);
    // Needed: current length + new string length + 1 (for the null terminator '\0')
    size_t needed_capacity = sb->length + str_len + 1; 
    
    // Check if we need to grow
    if (needed_capacity > sb->capacity) {
        size_t new_capacity = sb->capacity;
        
        // Double the capacity until it's large enough
        while (new_capacity < needed_capacity) {
            new_capacity *= 2;
        }
        
        // SAFE REALLOCATION: Use a temporary pointer!
        char *temp_data = (char*)realloc(sb->data, new_capacity);
        if (temp_data == NULL) {
            // Realloc failed, but the original sb->data is untouched and safe
            return false; 
        }
        
        // Apply the successful reallocation
        sb->data = temp_data;
        sb->capacity = new_capacity;
    }
    
    // Append the new string to the end of the existing data
    strcpy(sb->data + sb->length, str);
    sb->length += str_len;
    
    return true;
}

// 5. Destructor to prevent memory leaks
void sb_free(StringBuffer *sb) {
    if (sb != NULL) {
        free(sb->data); // Free the inside first
        free(sb);       // Free the outside last
    }
}

// 6. Demonstrate the requirements
int main() {
    printf("--- Dynamic String Buffer Demo ---\n\n");
    
    // Start with a very small capacity to force it to grow immediately
    StringBuffer *my_string = sb_init(10);
    if (!my_string) return 1;
    
    printf("Initial State:\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           my_string->data, my_string->length, my_string->capacity);
    
    // First append (fits inside initial 10 capacity)
    sb_append(my_string, "Hello");
    printf("After appending 'Hello':\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           my_string->data, my_string->length, my_string->capacity);
    
    // Second append (forces growth from 10 to 20)
    sb_append(my_string, ", World!");
    printf("After appending ', World!':\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           my_string->data, my_string->length, my_string->capacity);
           
    // Third append (forces growth from 20 to 40, then 80)
    sb_append(my_string, " Welcome to dynamic memory management in C.");
    printf("After appending long string:\n  String: \"%s\"\n  Length: %zu, Capacity: %zu\n\n", 
           my_string->data, my_string->length, my_string->capacity);
           
    // Clean up all memory
    sb_free(my_string);
    printf("Memory successfully freed.\n");
    
    return 0;
}