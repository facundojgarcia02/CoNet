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