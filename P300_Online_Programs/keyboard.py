import pickle
import pygame
import socket

from keyboard_dto import KeyboardDto

X_RECT_DIM = 100
Y_RECT_DIM = 100

X_RECT_MARGIN = 170
Y_RECT_MARGIN = 200

HOST, PORT = 'localhost', 9999

def init_keys(screen, font, key_list):
    key_dict = {}

    x_pos, y_pos = 100, screen.get_height()/2
    row, col = 0, 0
    for key in key_list:
        rect = pygame.Rect(x_pos + col * X_RECT_MARGIN, y_pos + row * Y_RECT_MARGIN, X_RECT_DIM, Y_RECT_DIM)
        txt = font.render(key, True, pygame.Color('white'))
        key_dict[key] = (txt, rect, False)

        col += 1
        if col >= 10:
            col = 0
            row += 1

    return key_dict

def display_keyboard(screen, font, key_dict, curr_text, suggestions):
    curr_display = font.render(curr_text, True, pygame.Color('white'))
    screen.blit(curr_display, (100, 100))

    suggestions_x_pos = 100
    for word_suggestion in suggestions:
        word_suggestion_text = font.render(word_suggestion, True, pygame.Color('white'))
        pygame.draw.rect(word_suggestion_text, pygame.Color('gray'), word_suggestion_text.get_rect(), 1)
        screen.blit(word_suggestion_text, (suggestions_x_pos, screen.get_height()/2 - 200))

        suggestions_x_pos += (screen.get_width() - 200)/5

    for key_params in key_dict.values():
        text = key_params[0]
        pygame.draw.rect(screen, pygame.Color('gray'), key_params[1])
        screen.blit(text, key_params[1])

    return key_dict

def main():

    pygame.init()

    pygame.display.set_caption("P300 GUI")
    screen = pygame.display.set_mode(size=(1920,1080))

    key_font = pygame.font.SysFont('Calibri', 90, True, False)
    word_font = pygame.font.SysFont('Calibri', 50, True, False)

    panogram = [c for c in 'QWERTYUIOPASDFGHJKLZXCVBNM'] + ['sp']
    key_dict = init_keys(screen, key_font, panogram)

    curr_text = ""

    running = True
    has_updated = True

    suggestions = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    if curr_text != "":
                        curr_text = curr_text[:-1]
                        has_updated = True
                elif event.unicode.isdigit():
                    suggestion_idx = int(event.unicode)

                    if suggestion_idx <= len(suggestions) and suggestion_idx != 0:
                        chosen_word = suggestions[suggestion_idx-1] + " "
                        string_split = curr_text.rsplit(" ", 1)
                        if len(string_split) == 1:
                            curr_text = chosen_word 
                        else:
                            curr_text = string_split[0] + " " + chosen_word 
                        
                        has_updated = True
                elif event.unicode.isalpha() or event.key == pygame.K_SPACE:
                    curr_text += event.unicode
                    has_updated = True
                else:
                    continue

        screen.fill(pygame.Color('black'))

        if has_updated:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))
                sent_keyboard_data = KeyboardDto(curr_text=curr_text)
                sock.send(pickle.dumps(sent_keyboard_data))
                received_keyboard_data = pickle.loads(sock.recv(4096))

            suggestions = received_keyboard_data.word_suggestions
            has_updated = False
            print("Probabilities of next character: ")
            for char, prob in received_keyboard_data.char_probs.items():
                print(f"'{char}': {round(prob, 4)}")
            print("=========================================")

        display_keyboard(screen, word_font, key_dict, curr_text, suggestions)

        pygame.display.update()
            
    pygame.quit()

if __name__ == "__main__":
    main()