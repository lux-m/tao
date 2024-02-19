import threading
import time
import requests


class BackgroundTask(threading.Thread):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            print("Executing background task...")
            try:
                # Simuler une requête à une API externe pour obtenir des données
                response = requests.get("https://api.github.com/repos/octocat/Spoon-Knife/issues")
                if response.status_code == 200:
                    data = response.json()
                    # Traiter les données récupérées
                    for item in data:
                        self.process_data_item(item)
                    print("Background task completed successfully.")
                else:
                    print(f"Failed to fetch data from API. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"An error occurred while fetching data from API: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            time.sleep(self.interval)

    def stop(self):
        self.is_running = False

    def process_data_item(self, item, process_func=None):
        """
        Process each data item individually using the provided processing function.

        Parameters:
            item (any): The data item to process.
            process_func (function): A function to apply to the data item. If None, no processing is done.
        """
        if process_func is None:
            print("No processing function provided. Skipping data item processing.")
            return

        try:
            processed_item = process_func(item)
            print(f"Processed data item: {processed_item}")
        except Exception as e:
            print(f"An error occurred while processing data item: {e}")


# Exemple de fonction de traitement personnalisée
def custom_process_func(item):
    """
    Custom processing function for data items.

    Parameters:
        item (any): The data item to process.

    Returns:
        any: The processed data item.
    """
    # Exemple de traitement : doubler la valeur de l'élément
    processed_item = item * 2
    return processed_item


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une instance de la tâche de fond avec un intervalle de 5 secondes
    background_task = BackgroundTask(interval=5)

    # Démarrer la tâche de fond
    background_task.start()

    # Attendre que la tâche de fond se termine (ce qui ne se produira jamais dans cet exemple)
    background_task.join()
