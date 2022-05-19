import multiprocessing as mp


def emetteur(sem):
	if proc_emet != []:
		for sem in proc_emet:
			sem.release()
	if proc_recept != []:
		for sem in proc_recept:
			sem.release()
	proc_recept.append(sem)


def recepteur(sem):
	if proc_emet != []:
                for sem in proc_emet:
                        sem.release()
        if proc_recept != []:
                for sem in proc_recept:
                        sem.release()
        proc_recept.append(sem)

