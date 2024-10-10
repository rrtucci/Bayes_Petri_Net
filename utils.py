import re

def get_gray_tone(num_grays, i):
    if i < 0 or i >= num_grays:
        raise ValueError("i should be in the range [0, num_grays]")
    tone_value = int((num_grays - i - 1) * 255 / (num_grays - 1))
    hex_value = f"{tone_value:02x}"  # Convert to 2-digit hex
    return f"#{hex_value}{hex_value}{hex_value}"  # Return the gray color

def get_label_value(str0):
    match = re.search(r'label=(\d+)', str0)
    if match:
        return int(match.group(1))
    else:
        return None

if __name__ == "__main__":
    def main():
        num_grays = 10
        print("gray_tones=",
            [get_gray_tone(num_grays, i) for i in range(num_grays)])
        str0 = "my name label=56is bob"
        print(get_label_value(str0))

    main()

