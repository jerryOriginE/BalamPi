import cv2
import numpy as np
import time
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path="model/model_unquantized.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open("model/labels.txt", "r") as f:
    labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]

cap = cv2.VideoCapture(0) # Abre la cámara web de la Raspberry Pi

print("¡Sistema Activo! Coloca un objeto frente a la cámara...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocesar la imagen para que coincida con lo que pide la IA (224x224 píxeles)
        img = cv2.resize(frame, (224, 224))
        img = np.expand_dims(img, axis=0)
        img = (img.astype(np.float32) / 127.5) - 1.0  # Normalización estándar de Teachable Machine

        # Pasar la imagen al modelo de TensorFlow Lite
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        
        # Obtener los resultados de predicción
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]
        max_index = np.argmax(predictions)
        material_detectado = labels[max_index]
        porcentaje_certeza = predictions[max_index] * 100

        # Si la IA está muy segura de lo que ve (más del 85% de certeza)
        if porcentaje_certeza > 85:
            # Mostramos en pantalla el resultado antes de mover motores
            texto = f"{material_detectado} ({porcentaje_certeza:.1f}%)"
            cv2.putText(frame, texto, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Camara Contenedor", frame)
            cv2.waitKey(1)

            # Pausamos la cámara momentáneamente y ejecutamos el movimiento físico
            #cap.release() 
            #cv2.destroyAllWindows()
            
            

            # Al terminar el movimiento, reabrimos la cámara para el siguiente ciclo
            #cap = cv2.VideoCapture(0)
        
        # Mostrar el video en tiempo real en el escritorio de la Raspberry Pi
        else:
            # Si la IA no está segura, mostramos un mensaje de "No estoy seguro"
            texto = f"No estoy seguro ({porcentaje_certeza:.1f}%)"
            cv2.putText(frame, texto, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Camara Contenedor", frame)
            cv2.waitKey(1)

        
        cv2.imshow("Camara Contenedor", frame)
        # Si presionan la tecla 'q', el programa se cierra de forma limpia
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nApagando el sistema de forma segura...")

finally:
    cap.release()
    cv2.destroyAllWindows()