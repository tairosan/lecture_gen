
import yaml
from lecture_generator import generate_lecture_content
from quiz_generator import generate_quiz_content

def main():
    # Read syllabus from YAML file
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # Open book.md for writing
    with open("book.md", "w") as book_file:
        # Iterate over each week in the syllabus
        for week in syllabus:
            week_number = week["week"]
            topics = week["topics"]
            lectures = week["lectures"]

            # Write week header
            book_file.write(f"# Week {week_number}: {', '.join(topics)}\n\n")

            # Iterate over each lecture in the week
            for lecture in lectures:
                title = lecture["title"]
                description = lecture["description"]

                # Generate lecture content using AI
                lecture_content = generate_lecture_content(title, description)

                # Generate quiz content using AI
                quiz_content = generate_quiz_content(title, description)

                # Write lecture content to book.md
                book_file.write(f"## {title}\n\n")
                book_file.write(f"{lecture_content}\n\n")

                # Write quiz content to book.md
                book_file.write(f"## Quiz: {title}\n\n")
                book_file.write(f"{quiz_content}\n\n")

if __name__ == "__main__":
    main()
