import os



blocks = []
with open("python-scripts/speaker_quotes.txt") as f:
    buffer = []
    current_speaker = None
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            if buffer and current_speaker:
                blocks.append({
                    "speaker": current_speaker,
                    "quotes": buffer
                })
            buffer = []
            current_speaker = None
        elif line.isdigit():
            current_speaker = line
        else:
            buffer.append(line)


# check
with open("majors.csv","w") as majors:
    majors.write("speaker, major\n")
    for b in blocks:
        print(f"Speaker: {b['speaker']}")
        for q in b['quotes']:
            print("  ", q)
        what_major = input("what major are they? ").lower()
        os.system('cls')
        majors.write(f"{b['speaker']}, {what_major}\n")
        print("---")

