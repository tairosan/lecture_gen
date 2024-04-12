from data.master_syllabus import syllabus
from utils.generator import generate_lectures

if __name__ == "__main__":
    generate_lectures(syllabus)
    print("Lecture materials generated successfully!")