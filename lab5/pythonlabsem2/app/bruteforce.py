import logging
import itertools
import hashlib  

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

tasks = {}

def generate_passwords(charset: str, max_length: int):
    for length in range(1, max_length + 1):
        for password_tuple in itertools.product(charset, repeat=length):
            yield "".join(password_tuple)


def bruteforce_task(task_id: str, hash_to_crack: str, charset: str, max_length: int):
    logging.debug(f"Task {task_id}: Starting bruteforce with hash: {hash_to_crack}, charset: {charset}, max_length: {max_length}")
    try:
        tasks[task_id]["status"] = "running"
        tasks[task_id]["progress"] = 0
        tasks[task_id]["result"] = None

        total_passwords = sum(len(list(itertools.product(charset, repeat=i))) for i in range(1, max_length + 1))
        passwords_tested = 0

        for password in generate_passwords(charset, max_length):
            passwords_tested += 1
            logging.debug(f"Task {task_id}: Testing password: {password}")

            current_password_hash = hashlib.sha256(password.encode()).hexdigest()

            if hash_to_crack == current_password_hash:
                tasks[task_id]["status"] = "completed"
                tasks[task_id]["progress"] = 100
                tasks[task_id]["result"] = password
                logging.info(f"Task {task_id}: Password found: {password}")
                print(f"Пароль найден: {password}")
                return

            progress = int((passwords_tested / total_passwords) * 100)
            tasks[task_id]["progress"] = progress

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["result"] = None
        logging.info(f"Task {task_id}: Password not found.")
        print("Пароль не найден.")

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = str(e)
        logging.error(f"Task {task_id}: Error: {e}", exc_info=True)
        tasks[task_id]["progress"] = 0
        print(f"Ошибка: {e}")
    finally:
        pass
