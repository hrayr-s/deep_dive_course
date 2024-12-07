#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <string.h>


int CHILD_PROCESS_ID;


char* addChar(char* str, char c)
{
    size_t len = strlen(str);
    str = realloc(str, len + 2);
    if (str == NULL)
    {
        free(str); // Free the old string if realloc fails
        perror("Memory allocation failed");
        return NULL;
    }

    str[len++] = c;

    str[len] = '\0';
    return str;
}

char **parseCommand2(const char *command) {
    char **args = malloc(3 * sizeof(char *)); // Allocate memory for two pointers
    if (args == NULL)
    {
        free(args); // Free the old string if realloc fails
        perror("Memory allocation failed");
        return NULL;
    }
    args[0] = malloc(sizeof(char *)); // Initialize firstArg
    args[1] = NULL;
    args[2] = NULL;

    int argc = 0;

    // Process firstArg
    for (int i = 0; command[i] != '\0'; i++) {
        if (command[i] == ' ') {
            argc = i + 1;
            break;
        }
        args[0] = addChar(args[0], command[i]);
    }

    // Process secondArg
    if (argc > 0)
    {
        args[1] = malloc(sizeof(char *)); // Initialize secondArg
        strcpy(args[1], &command[argc]);
    }

    return args;
}

// Signal handler function
void handle_sigint(int sig) {
    if (CHILD_PROCESS_ID > 0)
    {
        kill(CHILD_PROCESS_ID, SIGKILL);
        printf("Child process terminated\n");
    } else
    {
        printf("\nType exit and press Enter/Return to exit the micro bash.\n\n> ");
    }
    // exit(0); // Exit the program gracefully
}

int main()
{
    CHILD_PROCESS_ID = 0;
    // Install the signal handler for SIGINT
    signal(SIGINT, handle_sigint);

    char* command = NULL;
    char* exit_cmd = "exit";

    size_t len = 0;
    while (1)
    {
        printf("\n> ");
        ssize_t read = getline(&command, &len, stdin);
        if (read != -1)
        {
            // Remove the trailing newline character if present
            if (read > 0 && command[read - 1] == '\n')
            {
                command[read - 1] = '\0';
            }

            if (strcmp(command, exit_cmd) == 0)
            {
                break;
            }

            if (command[0] == '\0') continue; // skip empty enters

            CHILD_PROCESS_ID = fork();

            if (CHILD_PROCESS_ID == 0) {
                char **args = parseCommand2(command);
                execvp(args[0], args);
            } else {
                wait(NULL);
                CHILD_PROCESS_ID = 0;
            }
        }
        else
        {
            perror("getline failed");
        }
    }
    free(command);
    printf("Exiting...\n");
    return 0;
}
