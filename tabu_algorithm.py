import random
import time   # βιβλιοθήκη για τον υπολογισμού του χρόνου εκτέλεσης
import timeit
import requests  # βιβλιοθήκη για να παίρνει τα αρχεία απο το github
import os   # βιβλιοθήκη που παίρνει μόνο το όνομα του αρχείου από το file_path
from io import StringIO
import matplotlib.pyplot as plt   # βιβλιοθήκη για την σχεδίαση γραφημάτων
import matplotlib.colors as mcolors  # βιβλιοθήκη για την προσθήκη χρωμάτων στα γραφήματα
import matplotlib.dates as mdates

start_all = time.time()  # ο αρχικός χρόνος εκτέλεσης όλου του προγράμματος

# Δημιουργία μιας αρχικής λύσης με τυχαίο τρόπο
def generate_initial_solution(num_jobs):
    return random.sample(range(num_jobs), num_jobs)

# Υπολογισμός του χρονικού διαστήματος makespan ενός χρονοδιαγράμματος schedule
def calculate_makespan(schedule, processing_times):
    num_jobs = len(schedule)
    num_machines = len(processing_times[0])
    makespan = [0] * num_machines
    
    # Υπολογισμός του makespan για κάθε μηχανή
    for job in schedule:
        for i in range(num_machines):
            makespan[i] += processing_times[job][i]

    # Επιστρέφει το max makespan μεταξύ όλων των μηχανών
    return max(makespan)

# Συνάρτηση για να διαταραχθεί μια λύση με την ανταλλαγή δύο τυχαίων δεικτών
def perturb_solution(solution):
    # Δημιουργήστε δύο διαφορετικούς τυχαίους δείκτες από το εύρος του μήκους της λύσης
    idx1, idx2 = random.sample(range(len(solution)), 2)
    # Ανταλλάξτε τις τιμές στους τυχαία επιλεγμένους δείκτες της λύσης
    solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
    # Επιστρέψτε τη διαταραγμένη λύση
    return solution

# Tabu search algorithm
def tabu_search(processing_times, tabu_size, num_iterations):
    num_jobs = len(processing_times)
    current_solution = generate_initial_solution(num_jobs)
    current_makespan = calculate_makespan(current_solution, processing_times)

    best_solution = current_solution
    best_makespan = current_makespan

    tabu_list = []

    for iteration in range(num_iterations):
        new_solution = perturb_solution(current_solution)
        new_makespan = calculate_makespan(new_solution, processing_times)
        
        # Ελέγξτε αν η νέα λύση δεν είναι στη λίστα tabu και έχει μικρότερο makespan
        for solution in new_solution:
            
            if new_solution not in tabu_list and new_makespan < current_makespan:
                current_solution = new_solution
                current_makespan = new_makespan
                
                # Update την καλύτερη λύση αν το makespan βελτιωθεί
                if new_makespan < best_makespan:
                    best_solution = new_solution
                    best_makespan = new_makespan

        # Προσθήκη της νέας λύσης στη λίστα tabu
        tabu_list.append(new_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_solution

# Δημιουργία πίνακα χρόνων τερματισμού εκτέλεσης κάθε εργασίας σε κάθε μηχάνημα
def completion_time_table(schedule):
    if not isinstance(schedule[0], list):
        # If schedule is a 1D list, convert it to a 2D list
        schedule = [schedule]

    num_jobs, num_machines = len(schedule), len(schedule[0])
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


# πιο ακριβής μηχανισμός χρονισμού γιατί με την παραπάνω συνάρτηση κάποιες φορές εμφάνιζε 0.0 seconds
def count_time(algorithm, *args):
    elapsed_time = timeit.timeit(lambda: algorithm(*args), number=1)
    return elapsed_time


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
    if isinstance(file_path, list):
        # Handle each file path in the list
        result = []
        for path in file_path:
            result.extend(read_data_from_file(path))
        return result
    
    # Έλεγχος εάν το μονοπάτι αντιστοιχεί σε URL του GitHub   --- public or private  ---
    if file_path.startswith("https://github.com/penyvinni/AADS_PFSP_170/tree/main/Taillard-PFSP"):
        return read_data_from_github(file_path)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Διάβασμα όλων των γραμμών των αρχείων

        schedule = [list(map(int, line.strip().split()[1::2])) for line in lines[1::2]]  # Κάνει split τις διαστάσεις του προβλήματος στο schedule

        # Εξαγωγή των χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
        processing_times = [job[1:] for job in schedule]

    # Επιστρέφει μια λίστα με τα δεδομένα (processing times)
    return processing_times


# Διάβασμα αρχείων local από τον υπολογιστή μου
# def read_data_from_file(file_path):
#     for file_path in file_paths_tabu_search:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()  #διάβασμα όλων των γραμμών του αρχείου
        
#             schedule = map(int, lines[0].split())
        
#             # εξαγωγη  χρόνων επεξεργασίας των εργασιών από κάθε γραμμή, παραλείποντας την πρώτη γραμμή με τον αριθμό των εργασιών
#             processing_times = [list(map(int, line.strip().split()[1:])) for line in lines[1:]] 
        
#     # επιστροφή λίστας με τους χρόνους επεξεργασίας των εργασιών
#     return processing_times

# Εκτέλεση του αλγορίθμου tabu σε ένα συγκεκριμένο αρχείο
def run_tabu_search(file_path, tabu_size, num_iterations, output_file):
    processing_times = read_data_from_file(file_path)
    result_schedule = tabu_search(processing_times, tabu_size, num_iterations)
    makespan = calculate_makespan(result_schedule, processing_times)
    elapsed_time = count_time(tabu_search, processing_times,tabu_size, num_iterations)
    file_name = os.path.basename(file_path)
    C_table = completion_time_table(result_schedule)

    # Δημιουργία αρχείου txt για εγγραφή των αποτελεσμάτων
    with open(output_file, 'a', encoding='utf-8') as f:
        # Γράφει τα αποτελέσματα στο αρχείο
        f.write(f"File: {file_path}")
        f.write(f"\nTabu Search Makespan: {makespan}")  # Ο χρόνος εκτέλεσης Tabu Search
        f.write("\n\n\n")

    # Εκτυπώνει τα αποτελέσματα
    print(f"File: {file_path}")
    print("Tabu Search Optimal Schedule:", result_schedule)
    print("Tabu Search Makespan:", makespan)
    print("Processing times list is:", processing_times)
    print(f"\nExecution Time for {file_name} file: {elapsed_time} seconds")
    print("-----------------------------------------------------------------------------")
    print("\n")

def format_file_number(file_number):
    # Format file number with leading zeros
    return f"{file_number:03d}"

# Generate file paths with leading zeros
file_paths_tabu_search = [f'./Taillard-PFSP/ta{format_file_number(i)}.txt' for i in range(1, 21)]
processing_times = read_data_from_file(file_paths_tabu_search)

# Parameters for Tabu Search
tabu_size_tabu_search = 10
num_iterations_tabu_search = 1000

# Αποθήκευση των αποτελεσμάτων σε συγκεκριμένο Αρχείο
output_file = 'C:/Users/penyv/Desktop/DIT/Μεταπτυχιακό/Αλγόριθμοι & Προχωρημένες Δομές Δεδομένων/AADS_Vinni_170/code'
output_file = 'makespan_tabu_search.txt'

# Run Tabu Search for each file
for file_path_tabu_search in file_paths_tabu_search:
    run_tabu_search(file_path_tabu_search, tabu_size_tabu_search, num_iterations_tabu_search, output_file)

# Ο χρόνος εκτέλεσης όλου του προγράμματος
end_all = time.time()
elapsed_all = end_all - start_all
print(f"Total Execution Time: {elapsed_all} seconds")

# Διάγραμμα Gannt
def display_schedule(processing_times, makespan, C_table,file_name):
    num_jobs, num_machines = len(processing_times), len(processing_times[0])

    colors = list(mcolors.TABLEAU_COLORS.values())

    plt.figure(figsize=(10, num_machines * 3))
    for i in range(num_machines):
        job_start_time = 0
        for j in range(num_jobs):
            try:
                # Ανάκτηση χρόνου ολοκλήρωσης για κάθε εργασία
                completion_time = C_table[0][j]  # Άμεση πρόσβαση στο χρόνο ολοκλήρωσης
                job_start_time = max(completion_time, job_start_time)
                plt.barh(i, width=processing_times[j][i], left=job_start_time, height=0.8,
                         color=colors[j % len(colors)], label=f"Job {j}" if i == 0 else "")
            except IndexError as e:
                print(f"Error: {e}")
                print(f"i: {i}, j: {j}")

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.yticks(range(num_machines), [f"Machine {i}" for i in range(1, num_machines + 1)])
    plt.xlabel('Time')

    # Add the file name to the title of the chart
    plt.title(f'Permutation Flowshop Schedule NEH O(n^2m) - {file_name}')

    plt.legend(by_label.values(), by_label.keys(), loc="upper right")
    plt.gca().invert_yaxis()
    plt.show()
    
processing_times = read_data_from_file(file_paths_tabu_search)
result_schedule = tabu_search(processing_times, tabu_size_tabu_search, num_iterations_tabu_search)
makespan = calculate_makespan(result_schedule, processing_times)
elapsed_time = count_time(tabu_search, processing_times, tabu_size_tabu_search, num_iterations_tabu_search)
C_table = completion_time_table(result_schedule)
file_name = os.path.basename(file_paths_tabu_search[0])  # Χρησιμοποιεί το όνομα του πρώτου αρχείου
# Εμφάνιση του προγράμματος παραγωγής με γράφημα Gantt
display_schedule(processing_times, makespan, C_table, file_name)