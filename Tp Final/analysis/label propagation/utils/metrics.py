from collections import Counter

def accuracy(test_labels: dict, pred_labels: dict) -> float:
    """
    Calculate accuracy for propagated labels.
    """

    # Nos fijamos que etiquetas de testeo quedaron etiquetadas:
    found_test_labels = {n: l for n, l in test_labels.items() if n in pred_labels.keys()}

    # Nos fijamos si coinciden: 
    # Si en test hay varios tags para un nodo, nos fijamos que uno coincida por lo menos.
    coincidences = []
    errors = []
    for n, l in found_test_labels.items():
        if not isinstance(l, list):
            raise Exception("No debería de haber etiquetas que no sean listas.")          
        
        # Revisamos que la la etiqueta encontrada esté en la lista de las de testeo.
        if isinstance(pred_labels[n], str):
            if pred_labels[n] in l: 
                coincidences.append(n)
            else:
                errors.append(n)  
        
        # En caso de que sea una lista la encontrada, nos fijamos que haya una coincidencia por lo menos.
        elif isinstance(pred_labels[n], list):
            if len(set(pred_labels[n]).intersection(l)) > 0:
                coincidences.append(n)
            else:
                errors.append(n)
        
        #No debería de haber etiquetas propagadas que no sean str o list.
        else:
            raise Exception("No debería de haber etiquetas finales que no sean lista o str.")
    acc = len(coincidences)/(len(coincidences) + len(errors))
    print(f"Accuracy: {acc*100:.0f}%")

    return acc

def balanced_accuracy(test_labels: dict, pred_labels: dict) -> float:
    """
    Calculate Balanced Accuracy for propagated labels.
    """
    
    # Get topics and percentage of each in test set.
    label_collector = []
    for n, l in test_labels.items():
        label_collector += l

    topics = set(label_collector)
    test_fracs = {t: v/len(label_collector) for t, v in Counter(label_collector).items()}
    test_fracs = dict(sorted(test_fracs.items(), key = lambda x: x[1], reverse=True))
    
    # Init dicts.
    times_seen = {t: 0 for t in topics}
    matches = {t: 0 for t in topics}
    
    # Find nodes that were predicted.
    found_test_labels = {n: l for n, l in test_labels.items() if n in pred_labels.keys()}

    for n, l in found_test_labels.items():
        if not isinstance(l, list):
            raise Exception("No debería de haber etiquetas de testeo que no sean listas.")          

        # Revisamos que la la etiqueta encontrada esté en la lista de las de testeo.
        if isinstance(pred_labels[n], str):
            for _l in l:
                times_seen[_l] += 1
            if pred_labels[n] in l: 
                matches[pred_labels[n]] += 1

        # En caso de que sea una lista la encontrada, nos fijamos que haya una coincidencia por lo menos.
        elif isinstance(pred_labels[n], list):
            for _l in l:
                times_seen[_l] += 1
            if pred_labels[n] in l: 
                matches[pred_labels[n]] += 1

        #No debería de haber etiquetas propagadas que no sean str o list.
        else:
            raise Exception("No debería de haber etiquetas finales que no sean lista o str.")
    
    accuracy_per_topic = {t: matches[t]/times_seen[t] for t in topics}
    bal_acc = sum(accuracy_per_topic.values())/len(accuracy_per_topic.values())
    return bal_acc, times_seen