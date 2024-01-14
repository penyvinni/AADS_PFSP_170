import time    # βιβλιοθήκη για τον υπολογισμού του χρόνου εκτέλεσης
import timeit  # βιβλιοθήκη για να μετρήσει τον χρόνο εκτέλεσης με μεγαλύτερη ακρίβεια.
import requests  # βιβλιοθήκη για να παίρνει τα αρχεία απο το github
import os        # βιβλιοθήκη που παίρνει μόνο το όνομα του αρχείου από το file_path
import matplotlib.pyplot as plt   # βιβλιοθήκη για την σχεδίαση γραφημάτων
import matplotlib.colors as mcolors  # βιβλιοθήκη για την προσθήκη χρωμάτων στα γραφήματα

start_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος

# Υλοποήση του βελτιωμένου αλγορίθμου NEH για το πρόβλημα PFSP
def neh_square(jobs, job_sequence=None):
    
    n = len(jobs)  # n: Πλήθος των εργασιών
    machine = len(jobs[0])  # machine: Πλήθος των μηχανών

    # Αρχικός προγραμματισμός με βάση τον χρόνο εκτέλεσης (makespan)
    initial_schedule = list(range(n))
    initial_schedule.sort(key=lambda x: makespan_square([x] , jobs))
    
    # Αρχικοποίηση της καλύτερης διάταξης και του καλύτερου makespan
    best_schedule = initial_schedule 
    best_makespan = makespan_square(best_schedule , jobs)
    
    # Εξέταση κάθε δυνατού συνδυασμού για βελτιστοποίηση του makespan
    for i in range(1, n):
        current_n = initial_schedule[i]
        candidate_schedule = best_schedule[:i] + [current_n] + best_schedule[i:]
        candidate_makespan = makespan_square(candidate_schedule , jobs)
        if candidate_makespan < best_makespan:
            best_makespan = candidate_makespan
            best_schedule = candidate_schedule

    # Επιστροφή της βέλτιστης διάταξης και του βέλτιστου makespan
    return best_schedule, best_makespan

# Υπολογισμός του makespan για τον βελτιωμένο NEH για μια διάταξη
def makespan_square(schedule, jobs):
    n = len(schedule)
    machine = len(jobs[0])
    
    # Υπολογισμός των χρόνων ολοκλήρωσης για κάθε εργασία σε κάθε μηχάνημα
    completion_times = calculate_completion_times(schedule, jobs)
    
    # Επιστροφή του makespan, που βρίσκεται στο τέλος της τελευταίας στήλης του πίνακα
    return completion_times[-1][-1]

# Υπολογισμός των χρόνων ολοκλήρωσης για κάθε εργασία σε κάθε μηχάνημα
def calculate_completion_times(schedule, jobs):
    
    # Δημιουργία πίνακα με τους χρόνους ολοκλήρωσης, αρχικοποιημένους με μηδέν
    completion_times = [[0] * len(jobs[0]) for _ in range(len(schedule))]
    
    # Υπολογισμός των χρόνων ολοκλήρωσης
    for i, job in enumerate(schedule):
        for j in range(len(jobs[0])):
            if i == 0:
                completion_times[i][j] = jobs[schedule[i]][j]
            elif j == 0:
                completion_times[i][j] = completion_times[i-1][j] + jobs[schedule[i]][j]
            else:
                completion_times[i][j] = max(completion_times[i][j-1], completion_times[i-1][j]) + jobs[schedule[i]][j]

    # Επιστροφή των χρόνων ολοκλήρωσης
    return completion_times


# πιο ακριβής μηχανισμός χρονισμού γιατί με την παραπάνω συνάρτηση κάποιες φορές εμφάνιζε 0.0 seconds
def count_time(algorithm, *args):
    elapsed_time = timeit.timeit(lambda: algorithm(*args), number=1)
    return elapsed_time

# Διάβασμα αρχείων local από τον υπολογιστή μου
# def read_data_from_file(file_path):     
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         schedule = map(int, lines[0].split())
#         jobs = [list(map(int, line.strip().split())) for line in lines[1:]]

#     return jobs

# Εύρεση αρχείων στο GitHub και έλεγχος ύπαρξης
def read_data_from_github(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Έλεγχος εάν το request έγινε επιτυχώς
        content = response.text
        return content
    # Διαφορετικά εμφάνιση error μηνύματος
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
    return None

# Διάβασμα αρχείων από το GitHub
def read_data_from_file(file_path):
    # Έλεγχος εάν το μονοπάτι αντιστοιχεί σε URL του GitHub   --- public or private  ---
    if file_path.startswith("https://github.com/penyvinni/AADS_PFSP_170/tree/main/Taillard-PFSP"):
        return read_data_from_github(file_path)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()   # Διάβασμα όλων των γραμμών των αρχείων
        schedule = map(int, lines[0].split()) # Κάνει split τις διαστάσεις του προβλήματος στο schedule
        
        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        jobs = [list(map(int, line.strip().split()[1::2])) for line in lines[1::2]]
        
    # Επιστρέφει μια λίστα με τα δεδομένα (processing times)
    return jobs

# Κάλεσμα και εκτέλεση του βελτιωμένου αλγορίθμου NEH_square για όλα τα αρχεία
def run_neh_square(file_path):
    jobs_from_file = read_data_from_file(file_path)
    elapsed_time = count_time(neh_square, jobs_from_file)
    best_schedule, best_makespan = neh_square(jobs_from_file)
    file_name = os.path.basename(file_path)

    # Εκτύπωση των αποτελεσμάτων
    print(f"\nFile: {file_path}")
    print("\nJobs from File:", jobs_from_file)
    print("\nNEH Square O(n^2m) Optimal Jobs Order (Schedule):\n", best_schedule)
    print("\nNEH Square O(n^2m) Processing Time (Makespan):", best_makespan)
    print(f"\nExecution Time for {file_name} file: {elapsed_time} seconds")
    print("\n")
    print("-----------------------------------------------------------------------------")
    print("\n")


# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"

# Δημιουργία λίστας με file paths που ξεκινούν από το ta001.txt έως το ta120.txt
file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(20, 21)]

# Εκτέλεση αλγορίθμου NEH για κάθε αρχείο
for file_path in file_paths:
    run_neh_square(file_path)

# Ο χρόνος εκτέλεσης όλου του προγράμματος 
end_all = time.time()
elapsed_all = end_all - start_all
print(f"Total Execution Time: {elapsed_all} seconds")


#Δημιουργία γραφήματος Gantt για τα αρχεία
def display_schedule(jobs, best_schedule, file_name):
    num_jobs, num_machines = len(jobs), len(jobs[0])
    completion_times = calculate_completion_times(best_schedule, jobs)
    colors = list(mcolors.TABLEAU_COLORS.values())

    plt.figure(figsize=(10, num_machines * 3))
    for i in range(num_machines):
        for j in best_schedule:
            job_start_time = completion_times[j][i] - jobs[j][i]
            plt.barh(i, width=jobs[j][i], left=job_start_time, height=0.8, color=colors[j % len(colors)],
                     label=f"Job {j}" if i == 0 else "")

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.yticks(range(num_machines), [f"Machine {i}" for i in range(1, num_machines + 1)])
    plt.xlabel('Time')
    
    # Add the file name to the title of the chart
    plt.title(f'Permutation Flowshop Schedule NEH O(n^2m) - {file_name}')
    
    plt.legend(by_label.values(), by_label.keys(), loc="upper right")
    plt.gca().invert_yaxis()
    plt.show()
    
             
jobs_from_file = read_data_from_file(file_path)
best_schedule, best_makespan = neh_square(jobs_from_file)
jobs = read_data_from_file(file_path)
file_name = os.path.basename(file_path)
# Call the modified display_schedule function
display_schedule(jobs_from_file, best_schedule, file_name)