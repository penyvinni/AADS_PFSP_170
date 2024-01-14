import time   # βιβλιοθήκη για τον υπολογισμού του χρόνου εκτέλεσης
import timeit  # timeit για να μετρήσει τον χρόνο εκτέλεσης με μεγαλύτερη ακρίβεια.
import matplotlib.pyplot as plt # βιβλιοθήκη για την σχεδίαση γραφημάτων
import matplotlib.colors as mcolors  # βιβλιοθήκη για την προσθήκη χρωμάτων στα γραφήματα
import requests  # βιβλιοθήκη για να παίρνει τα αρχεία απο το github
import os   # βιβλιοθήκη που παίρνει μόνο το όνομα του αρχείου από το file_path
import numpy as np
from io import StringIO

start_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος

# Υλοποίηση του αλγορίθμου NEH
def neh_algorithm(jobs, job_sequence=None):
    # Ταξινόμηση των εργασιών με βάση το άθροισμά τους (φθίνουσα σειρά)
    jobs.sort(key=lambda x: sum(x), reverse=True)
    
    # Αρχικοποίηση του προγράμματος με τις δύο πρώτες εργασίες
    schedule = [jobs[0], jobs[1]]
    
    # Εάν παρέχεται η σειρά job_sequence, χρησιμοποιείται ως αρχική σειρά
    if job_sequence:
        jobs = [jobs[i] for i in job_sequence]

    # Επεξεργασία των υπολοίπων εργασιών
    for i in range(2, len(jobs)):
        best_schedule = None
        best_makespan = float('inf')

        # Εισαγωγή τρέχουσας εργασίας i σε διαφορετικές θέσεις στο χρονοδιάγραμμα (schedule)
        for j in range(len(schedule) + 1):
            candidate_schedule = schedule[:j] + [jobs[i]] + schedule[j:]  # Υπολογισμός του προτεινόμενου χρονοπρογράμματος
            candidate_makespan = calculate_makespan(candidate_schedule)   # Υπολογισμός του makespan για το προτεινόμενο πρόγραμμα

            # Αν το προτεινόμενο schedule  έχει μικρότερο makespan, αποθηκεύεται ως το καλύτερο
            if candidate_makespan < best_makespan:
                best_makespan = candidate_makespan
                best_schedule = candidate_schedule

        # Ενημέρωση του προγράμματος με το καλύτερο schedule για την εργασία i
        schedule = best_schedule
    
    # Επιστροφή του καλύτερου προγράμματος και του αντίστοιχου makespan
    return schedule, best_makespan

# Υπολογισμός του χρόνου επεξεργασίας makespan 
def calculate_makespan(schedule):
    
    # Ορισμός των αριθμών των εργασιών και των μηχανών κάθε αρχείου αντίστοιχα
    num_jobs = len(schedule)
    num_machines = len(schedule[0])
    # Ορισμός πίνακα με διαστάσεις jobs x machines 
    completion_times = [[0] * num_machines for _ in range(num_jobs)]

    # Υπολογισμός χρόνων ολοκλήρωσης για την πρώτη μηχανή
    completion_times[0][0] = schedule[0][0]
    for j in range(1, num_jobs):
        completion_times[j][0] = completion_times[j-1][0] + schedule[j][0]

    # Υπολογισμός χρόνων ολοκλήρωσης για τις υπόλοιπες μηχανές
    for i in range(1, num_machines):
        completion_times[0][i] = completion_times[0][i-1] + schedule[0][i]
    
    for j in range(1, num_jobs):
        for i in range(1, num_machines):
            completion_times[j][i] = max(completion_times[j-1][i], completion_times[j][i-1]) + schedule[j][i]

    # Το makespan είναι ο χρόνος ολοκλήρωσης της τελευταίας εργασίας στην τελευταία μηχανή
    makespan = completion_times[num_jobs-1][num_machines-1]

    return makespan

# Υπολογισμός του χρόνου εκτέλεσης του αλγορίθμου για κάθε αρχείο
def count_time(algorithm, *args):
    elapsed_time = timeit.timeit(lambda: algorithm(*args), number=1)
    return elapsed_time

# Δημιουργία πίνακα χρόνων τερματισμού εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
def completion_time_table(schedule):
    num_jobs = len(schedule)
    num_machines = len(schedule[0])
    C = [[0] * num_machines for _ in range(num_jobs)]

    # Calculate completion times for the first machine
    C[0][0] = schedule[0][0]
    for j in range(1, num_jobs):
        C[j][0] = C[j-1][0] + schedule[j][0]

    # Calculate completion times for the remaining machines
    for i in range(1, num_machines):
        C[0][i] = C[0][i-1] + schedule[0][i]

    for j in range(1, num_jobs):
        for i in range(1, num_machines):
            C[j][i] = max(C[j-1][i], C[j][i-1]) + schedule[j][i]

    return C



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
        lines = file.readlines()  # Διάβασμα όλων των γραμμών των αρχείων

        schedule = map(int, lines[0].split())  # Κάνει split τις διαστάσεις του προβλήματος στο schedule

        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        jobs = [list(map(int, line.strip().split()[1::2])) for line in lines[1::2]]

    # Επιστρέφει μια λίστα με τα δεδομένα (processing times)
    return jobs

# Διάβασμα αρχείων local από τον υπολογιστή μου
# def read_data_from_file(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()  #διάβασμα όλων των γραμμών του αρχείου
        
#         schedule = map(int, lines[0].split())
        
#         # εξαγωγη  χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
#         jobs = [list(map(int, line.strip().split()[1:])) for line in lines[1:]] 
        
#     # επιστροφή λίστας με τους χρόνους επεξεργασίας των εργασιών
#     return jobs

# Μορφοποίηση αριθμού αρχείου που ξεκινάει με μηδενικά
def format_file_number(file_number):
    return f"{file_number:03d}"

# Κάλεσμα και εκτέλεση του αλγορίθμου NEH για όλα τα αρχεία
def run_neh_algorithm(file_path, output_file):
    
    jobs_from_file = read_data_from_file(file_path)
    
    best_schedule, best_makespan = neh_algorithm(jobs_from_file)
    jobs = read_data_from_file(file_path)
    
    # Εκτέλεση του αλγορίθμου NEH με τη σειρά job_sequence για τη λήψη της σωστής σειράς των εργασιών
    optimal_order, _ = neh_algorithm(jobs_from_file, job_sequence=range(len(jobs_from_file)))
    
    elapsed_time = count_time(neh_algorithm, jobs_from_file)
    
    file_name = os.path.basename(file_path)
    
    C_table = completion_time_table(best_schedule)
    
    # Extract indices of jobs in the original list from the optimal_order list
    # Εξαγωγή των δεικτών των θέσεων εργασίας της αρχικής λίστας από τη λίστα optimal_order
    optimal_order_indices = [jobs_from_file.index(job) for job in optimal_order]

    # Δημιουργία αρχείου txt για εγγραφή των αποτελεσμάτων
    with open(output_file, 'a', encoding='utf-8') as f:
        # Γράφει τα αποτελέσματα στο αρχείο
        f.write(f"File: {file_path}")
        f.write(f"NEH Search Makespan: {best_makespan}")  # Ο χρόνος εκτέλεσης Tabu Search
        f.write("\n\n\n")

    # Εκτύπωση των αποτελεσμάτων
    print(f"\nFile: {file_path}")
    print("\nNEH Optimal Jobs Order (Schedule):\n", best_schedule)
    print("\nNEH Correct Jobs Order (Job Indices):", optimal_order_indices)
    print("\nNEH Processing Time (Makespan):", best_makespan)
    print(f"\nExecution Time for {file_name} file: {elapsed_time} seconds")
    print("\nCompletion Times Table:")
    for row in C_table:
        print(row)  # Εμφάνιση κάθε γραμμής του πίνακα C_table (τους χρόνους τερματισμού εκτέλεσης)
    print("\n")
    print("-----------------------------------------------------------------------------")
    print("\n")
    

# Δημιουργία λίστας με file paths που ξεκινούν από το ta001.txt έως το ta120.txt
file_paths = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 21)]

# Αποθήκευση των αποτελεσμάτων σε συγκεκριμένο Αρχείο
output_file = 'C:/Users/penyv/Desktop/DIT/Μεταπτυχιακό/Αλγόριθμοι & Προχωρημένες Δομές Δεδομένων/AADS_Vinni_170/code'
output_file = 'makespan_neh_algorithm.txt'

# Εκτέλεση αλγορίθμου NEH για κάθε αρχείο
for file_path in file_paths:
    run_neh_algorithm(file_path, output_file)
    
# Ο χρόνος εκτέλεσης όλου του προγράμματος 
end_all = time.time()
elapsed_all = end_all - start_all
print(f"Total Execution Time: {elapsed_all} seconds")
    


# Δημιουργία γραφήματος Gantt για τα αρχεία
def display_schedule(schedule, optimal_order_indices):
    num_jobs, num_machines = len(schedule), len(schedule[0])
    colors = list(mcolors.TABLEAU_COLORS.values())

    plt.figure(figsize=(10, num_machines * 3))
    for i in range(num_machines):
        for j in optimal_order_indices:
            job_start_time = C_table[j][i] - schedule[j][i]
            plt.barh(i, width=schedule[j][i], left=job_start_time, height=0.8, color=colors[j % len(colors)],
                     label=f"Job {j}" if i == 0 else "")

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.yticks(range(num_machines), [f"Machine {i}" for i in range(1, num_machines + 1)])
    plt.xlabel('Time')
    
    # Προσθήκη του ονόματος του αρχείου στον τίτλο του γραφήματος
    plt.title(f'Permutation Flowshop Schedule NEH O(n^3m) - {file_name}')
    
    plt.legend(by_label.values(), by_label.keys(), loc="upper right")
    plt.gca().invert_yaxis()
    plt.show()


jobs_from_file = read_data_from_file(file_path)
best_schedule, best_makespan = neh_algorithm(jobs_from_file)
optimal_order, _ = neh_algorithm(jobs_from_file, job_sequence=range(len(jobs_from_file)))
elapsed_time = count_time(neh_algorithm, jobs_from_file)
file_name = os.path.basename(file_path)
C_table = completion_time_table(best_schedule)
optimal_order_indices = [jobs_from_file.index(job) for job in optimal_order]
# Εκτύπωση του γραφήματος
display_schedule(best_schedule, optimal_order_indices)