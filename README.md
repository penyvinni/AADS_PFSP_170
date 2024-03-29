# Permutation Flow-shop Scheduling Problem (PFSP)
☑ Η παρούσα εργασία αναλύει το πρόβλημα PFSP (Permutation Flow Shop Scheduling Problem)
με στόχο την εξέταση και την επίλυσή του μέσω διαφόρων αλγορίθμων.

☑ Εφαρμόζεται ο ευρετικός αλγόριθμος NEH για την αρχική επίλυση, ακολουθούμενη από τη
βελτιστοποίηση του αλγορίθμου σύμφωνα με προηγούμενες προτάσεις.

☑ Στη συνέχεια, προτείνεται μια προσωπική προσέγγιση (Tabu Algorithm), συγκρίνοντάς την με τα αποτελέσματα του NEH.

## Ορισμός του προβλήματος PFSP
Το πρόβλημα **Permutation Flow-shop Scheduling Problem (PFSP)** είναι γνωστό ως είναι πρόβλημα χρονοπρογραμματισμού. 
Σε αυτό το σενάριο, ένα σύνολο n εργασιών (jobs) πρέπει να επεξεργαστεί με συγκεκριμένη σειρά σε m μηχανές (machines). 

Ο πρωταρχικός στόχος του συγκεκριμένου προβλήματος είναι να ελαχιστοποιηθεί ο χρόνος από την έναρξη της πρώτης εργασίας στην πρώτη μηχανή 
έως την ολοκλήρωση της τελευταίας εργασίας στην τελευταία μηχανή, που αναφέρεται ως χρόνος παραγωγής ή αλλιώς **makespan**.

Όσον αφορά τώρα τις πραγματικές εφαρμογές του προβλήματος PFSP, αυτές περιλαμβάνουν:
* Manufacturing (Βιομηχανία), 
* Logistics and Transportation (Μεταφορές) και
* Job Scheduling in Computing (Χρονοπρογραμματισμός εργασιών στην πληροφορική)

## Ο Αλγόριθμος NEH
Ο αλγόριθμος NEH είναι ένας ευρετικός αλγόριθμος που έχει σχεδιαστεί για την
αντιμετώπιση του προβλήματος προγραμματισμού ροής-καταστήματος μεταβολής (PFSP).
Ο αλγόριθμος NEH είναι γνωστός για την απλότητα και την αποτελεσματικότητά
του στη δημιουργία σχεδόν βέλτιστων λύσεων για περιπτώσεις PFSP.

Το αρχείο που περιέχει την υλοποίηση του αλγορίθμου NEH ονομάζεται `neh_algorithm` και εκτελείται ως εξής:
```
python neh_algorithm.py
```
## Ο Βελτιωμένος Αλγόριθμος NEH Ο(n^2m) 
Στο πρόγραμμα nehsquare.py η συγκεκριμένη υλοποίηση επιτυγχάνει τη βελτιστοποίηση του αλγορίθμου NEH, πετυχαίνοντας πολυπλοκότητα O(n∧2m). 
Η αποτελεσματικότητα και η απόδοση του αλγορίθμου αξιολογούνται μέσω της εκτύπωσης των βέλτιστων διατάξεων, 
των χρόνων εκτέλεσης και άλλων στατιστικών πληροφοριών για κάθε πρόβλημα.

Είναι σημαντικό να τονιστεί όμως, ότι η βελτιωμένη υλοποίηση του NEH αλγορίθμου
προσφέρει αξιοσημείωτη απόδοση και αποτελεσματικότητα, καθιστώντας τον αλγόριθμο
κατάλληλο για εφαρμογές μεγάλης κλίμακας στον τομέα της χρονοπρογραμματισμού παραγωγικών διεργασιών.

Το αρχείο που περιέχει την υλοποίηση του βελτιωμένου αλγορίθμου NEH ονομάζεται `neh_square` και εκτελείται ως εξής:
```
python neh_square.py
```
## Ο Meta-Heuristic Αλγόριθμος Tabu 
Ο αλγόριθμος Tabu Search είναι ένας βελτιωμένος μεταευριστικός (metaheuristic) αλγόριθμος που επιδιώκει την εύρεση
βέλτιστων λύσεων σε προβλήματα συνδυαστικής βελτιστοποίησης.
Λειτουργεί με τη χρήση μιας λίστας ”Tabu” που περιέχει κινήσεις οι οποίες έχουν προσφάτως εξεταστεί, αποφεύγοντας έτσι την επανάληψη των ίδιων κινήσεων.
Επιπλέον, χρησιμοποιεί μηχανισμούς όπως η λειτουργία κόστους για την επιλογή βέλτιστων κινήσεων.

Στην πράξη, ο αλγόριθμος Tabu Search ξεκινάει από μια αρχική λύση και εξερευνά διάφορες γειτονικές λύσεις. Οι καλύτερες λύσεις διατηρούνται, ακόμη κι αν αυτές προσθέτουν
κινήσεις που βρίσκονται στη λίστα Tabu. Ο αλγόριθμος εξερευνά διάφορες περιοχές του
χώρου λύσεων, προσπαθώντας να αποφύγει τον εγκλωβισμό.

Το αρχείο που περιέχει την υλοποίηση του αλγορίθμου Tabu ονομάζεται `tabu_algorithm` και εκτελείται ως εξής:
```
python tabu_algorithm.py
```
## 📊 Απεικόνιση Λύσεων με Γραφήματα Gantt


ς μηχανές στον άξονα y και τις εργασίες ως επιμέρους κουτάκια στις κατάλληλες θέσεις,
υλοποιήθηκε με τη χρήση της βιβλιοθήκης **Matplotlib** στην Python. 

Η Matplotlib είναι μία από τις πιο δημοφιλείς βιβλιοθήκες γραφικών στην Python και παρέχει ευέλικτα εργαλεία
για τη δημιουργία διαγραμμάτων και γραφημάτων. Συγκεκριμένα, η χρήση της Matplotlib
στον κώδικα περιλαμβάνει την εισαγωγή των εξής μετασχηματιστών:
```
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
```
Με τη χρήση αυτών των βιβλιοθηκών, η συνάρτηση `display_schedule` δημιουργεί
γραφήματα Gantt για την οπτικοποίηση των προγραμμάτων εκτέλεσης των εργασιών, βελτιώνοντας την κατανόηση των αποτελεσμάτων του αλγορίθμου Flowshop Scheduling.

Στην παρακάτω εικόνα απεικονίζεται ένα γράφημα Gantt το οποίο αντιστοιχείζεται με την λύση του αλγορίθμου ***NEH*** για το πρώτο αρχείο `ta001.txt` :

<img src="https://github.com/penyvinni/AADS_PFSP_170/blob/main/neh_run_ta001_gantt.png" width="500">
