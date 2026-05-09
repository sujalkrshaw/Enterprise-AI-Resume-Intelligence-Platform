import os


# LOAD JOB DESCRIPTION

def load_job_description(filepath):

    with open(filepath, "r", encoding="utf-8") as file:

        job_description = file.read()

    return job_description


# LOAD ALL RESUMES

def load_resumes(folder_path):

    resumes = []

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as file:

            content = file.read()

            resumes.append({

                "filename": filename,
                "content": content

            })

    return resumes


# TESTING

if __name__ == "__main__":

    jd = load_job_description(
        "job_descriptions/data_analyst.txt"
    )

    resumes = load_resumes("resumes")

    print("\nJOB DESCRIPTION:\n")
    print(jd)

    print("\nTOTAL RESUMES LOADED:", len(resumes))

    for resume in resumes:

        print("\n-------------------")
        print("Resume:", resume["filename"])
        print(resume["content"])