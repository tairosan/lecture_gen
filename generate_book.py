
import yaml
from lecture_generator import generate_lecture_content
from quiz_generator import generate_quiz_content

def main():
    # Read syllabus from YAML file
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # Open book.md for writing
    with open("book.md", "w") as book_file:
        # Process each week
        for week in syllabus:
            week_title = f"Week {week['week']}: {', '.join(week['topics'])}"
            book_file.write(f"# {week_title}\n\n")

            # Generate lecture content for each lecture
            for lecture in week['lectures']:
                lecture_title = lecture['title']
                lecture_description = lecture['description']
                lecture_content = generate_lecture_content(lecture_title, lecture_description)
                book_file.write(f"## {lecture_title}\n\n")
                book_file.write(lecture_content)
                book_file.write("\n\n")

            # Generate quiz content for the week
            quiz_content = generate_quiz_content(week_title, week['topics'])
            book_file.write("## Weekly Quiz\n\n")
            book_file.write(quiz_content)
            book_file.write("\n\n")

if __name__ == "__main__":
    main()
