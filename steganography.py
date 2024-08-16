from PIL import Image

def hide_message(input_path, message, output_path):
    
    image = Image.open(input_path)
    image_encoded = image.copy()
    
    message += '\0'
    message_encoded = message.encode('utf-8')

    message_bin = ''.join(format(byte,'08b') for byte in message_encoded)

    width, height = image.size
    index = 0

    for x in range(width):
        for y in range(height):
            pixel = list(image.getpixel((x,y)))
            for i in range(3):
                if index < len(message_bin):
                    pixel[i] = int(bin(pixel[i])[2:-1] + message_bin[index], 2)
                    index += 1
            image_encoded.putpixel((x,y), tuple(pixel))
            if index >= len(message_bin):
                break
        if index >= len(message_bin):
            break
    image_encoded.save(output_path)
    print("Pomyślnie ukryto wiadomość")


hide_message('puppy.jpg','ść','puppy2.png')

def reveal_message(image_path):
    image = Image.open(image_path)

    width, height = image.size

    message_bin = ""


    for x in range(width):
        for y in range(height):
            pixel = list(image.getpixel((x,y)))
            for i in range(3):
                message_bin += bin(pixel[i])[-1]

    byte_string = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i + 8]
        byte_string += byte
        byte_string += " "
    
    binary_data = byte_string.split()

    binary_data_cut = []
    for c in binary_data:
        decimal = int(c,2)
        char = chr(decimal)
        if char == '\0':
            break
        binary_data_cut.append(c)

    binary_data_array = bytearray(int(byte, 2) for byte in binary_data_cut)
    try:
        # Decode the byte array as a UTF-8 string
        message = binary_data_array.decode('utf-8')
    except UnicodeDecodeError as e:
        message = f"Error decoding message: {e}"
        print(message)

    return(message)
message = reveal_message('puppy2.png')
print(message)