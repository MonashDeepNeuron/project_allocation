

import pandas as pd
import numpy as np


def allocate_projects(students: list[str], projects:list[str], preferences: dict[str, list[str]]) -> dict[str, list[tuple[str, int]]]:
    """
    This function allocate the students to the projects based on their preference using the Gale-Shapley algorithm, or the Stable Marriage algorithm
    Preferences of student should have the same length, this guarantee that the function works without no unallocated students

    Args:
        students (list[str]): a list of students
        projects (list[str]): a list of projects
        preferences (dict[str, list[str]]): preference of each students, index 0 is the most preferred project

    Returns:
        dict[str, list[str]]: the project allocation, each project corresponds to a list of 2-tuples, containing the student's name
                                and the rank of that project in the preference of that student
    """


    # initialize the project allocation dictionary
    project_allocations = {project: [] for project in projects}

    # calculate the max capacity
    max_capacity = len(students) // len(projects)
    if len(students) % len(projects) != 0:
        max_capacity += 1

    # create a list to keep track of the allocated students
    student_number = len(students)
    allocated_students = []

    index = 0
    while len(allocated_students) < student_number:
        # PRINT FOR DEBUGGING
        # print("PROJECT ALLOCATIONS")
        # for project in project_allocations:
        #     print(project, project_allocations[project])
        
        # print("STUDENTS")
        # print(len(students), students)

        # print("PREFERENCES")
        # for student in students:
        #     print(preferences[student])

        # print("INDEX")
        # print(index)
        # print("___________")
        student = students[index]

        # keep track of the rank of the current project in the current student's preference
        rank = 1

        allocated = False
        for project in preferences[student]:
            current_capacity = len(project_allocations[project])

            # if the current project still has room, add the student to that project
            if current_capacity < max_capacity:
                project_allocations[project].append((student, rank))

                # add the students to the allocated students list and remove them from the unallocated one
                allocated_students.append(student)
                students.remove(student)
                allocated = True
            
            # if the current project is full, we need to check for preference
            if current_capacity == max_capacity:
                for allocation in project_allocations[project]:
                    # if there is a student who is already inside the current project and their preference for it 
                    # is less than the current student, remove that student and add the current student to the project
                    if allocation[1] > rank:
                        project_allocations[project].remove(allocation)
                        project_allocations[project].append((student, rank))


                        allocated_students.append(student)
                        allocated_students.remove(allocation[0])

                        students.remove(student)
                        students.append(allocation[0])

                        allocated = True
                        break
            
            # break the for loop if the student is allocated
            if allocated:
                break

            # increase the ranke if not allocated
            else:
                rank += 1
        else:
            # if the for loop is finished without breaking, the students cannot be allocated, this could be because that student did not fill in all of the prefence
            # increase the index
            index += 1
        
        # if reach the end of array, break the while loop
        if index >= len(students):
            break
                

    for project in project_allocations:
        while len(project_allocations[project]) < max_capacity:
            project_allocations[project].append(None)
            

    return project_allocations, students, {student: preferences[student] for student in students}

if __name__ == "__main__":
    # Example usage
    # students = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
    # projects = ['P1', 'P2', 'P3']
    # preferences = {
    #     'S1': ['P1', 'P2', 'P3'],
    #     'S2': ['P1', 'P3', 'P2'],
    #     'S3': ['P1', 'P2', 'P3'],
    #     'S4': ['P1', 'P2', 'P3'],
    #     'S5': ['P3', 'P2', 'P1'],
    #     'S6': ['P2', 'P3', 'P1'],
    # }
    # allocations = allocate_projects(students, projects, preferences)
    # print(allocations)

    df = pd.read_csv("preference.csv")
    students = df["Name"]
    projects = [
        "Project Preference [Parallel Training]",
        "Project Preference [Artifacts Digitization]",
        "Project Preference [Tune LLMs]",
        "Project Preference [Music Generation]",
        "Project Preference [ArtGAN]",
        "Project Preference [RL]",
        "Project Preference [CNN]",
        "Project Preference [NLP]",
    ]

    
    preferences = dict()
    for i, name in enumerate(students):
       
        pref = []

        for project in projects:
            if not np.isnan(df[project][i]):
                pref.append((df[project][i], project))

        pref.sort(key = lambda x: x[0], reverse=True)
        pref = [x[1] for x in pref]

        preferences[name] = pref


    allocations, students_left, preferences_left = allocate_projects(list(students), projects, preferences)

    print("PROJECT PREFERENCE")
    for project in allocations:
        print(project, allocations[project])

    print("STUDENTS LEFT")
    print(students_left)
    for project in preferences_left:
        print(project, preferences_left[project])


    allocations_df = pd.DataFrame.from_dict(allocations)
    allocations_df.to_csv("result.csv")
    

    
        

        

