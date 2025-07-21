import pandas as pd
import random

# Load Kanji data
csv_path = r"C:/Users/peter/Desktop/Peter/study stuff/DS/Kanji_Study_app/Kanji_Data/N3_kanji.csv"
df = pd.read_csv(csv_path)

total_kanji = len(df)
print(f"\n📘 Total Kanji available: {total_kanji}")
# print("🗒️ Note: Index starts from 1")

# Ask user for start and end index
while True:
    try:
        start = int(input("🔢 Enter starting index : "))
        end = int(input("🔢 Enter ending index : "))
        if 1 <= start <= end <= total_kanji:
            break
        else:
            print(f"⚠️ Please enter values between 1 and {total_kanji}, with start <= end.")
    except ValueError:
        print("❌ Please enter valid numbers.")

# Slice the DataFrame (adjusting for 0-based indexing)
quiz_data = df.iloc[start-1:end].sample(frac=1).reset_index(drop=True)  # Shuffle

print(f"\n🎌 Starting Kanji Quiz for Kanji {start} to {end} ({len(quiz_data)} questions)")
print("📝 Type the *meaning* of the Kanji. Press Enter to skip.\n")

score = 0

for i, row in quiz_data.iterrows():
    print(f"{i+1}. Kanji: {row['Kanji']}")
    answer = input("Your answer: ").strip().lower()
    correct = row["Meaning"].strip().lower()

    if answer == "":
        print(f"   ➤ Skipped. Meaning: {correct}\n")
    elif answer == correct:
        print("   ✅ Correct!\n")
        score += 1
    else:
        print(f"   ❌ Incorrect. Correct Meaning: {correct}\n")

# Final score
print(f"🎯 Quiz complete! You scored {score}/{len(quiz_data)} ({(score/len(quiz_data))*100:.1f}%)\n")
