import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()

    #Process next char
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0' #EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    #Return the lookahead char
    def peek(self):
        if self.cur_pos+1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos+1]

    #Invalid token found, print error and exit
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    #Skip whitespace except newlines
    def skip_whitespace(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()

    #Skip comments
    def skip_comments(self):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next_char()

    #Return next token
    def get_token(self):
        self.skip_whitespace()
        self.skip_comments()
        token = None

        #Check first char of this token to detect type
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword
        # then we will process the rest.
        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)

        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)

        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)

        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)

        elif self.cur_char == '=':
            #Check for '=='
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)

        elif self.cur_char == '>':
            #Check wether token is '>' or '>='
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.GT)

        elif self.cur_char == '<':
            #Check wether token is '<' or '<='
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.LTEQ)
            else:
                token = Token(self.cur_char, TokenType.LT)

        elif self.cur_char == '!':
            if self.peek() == '=':
                last_char = self.cur_char
                self.next_char()
                token = Token(last_char+self.cur_char, TokenType.NOTEQ)
            else:
                self.abort("Expected '!=', got '!'" + self.peek())

        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)

        elif self.cur_char == '\0':
            token = Token('', TokenType.EOF)



        else:
            #Unknown token
            self.abort("Unknown token: " + self.cur_char)

        self.next_char()
        return token


#Tokenizer, put in seperate file
class Token:
    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind

#Token type class
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    #Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    #Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
