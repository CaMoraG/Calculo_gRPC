import grpc
import server_pb2 as spb2
import server_pb2_grpc as sgrpc


def run(array):
    print("Arreglo sin ordenar: ", array)
    # Conexión con el servidor de calculo
    with grpc.insecure_channel('10.43.100.120:12345') as channel:
        stub = sgrpc.SortServiceStub(channel)
        response = stub.DivideAndMerge(spb2.Array(data=array))
        # Impresion del arreglo, accediendo al arreglo de la información recibida
        print("Arreglo ordenado:", response.data)


def initialize_array():
    n = int(input("Ingrese el tamaño del arreglo: "))
    array = []
    print("Introduzca los numeros del arreglo de tamaño ", n)

    for i in range(n):
        m = int(input())
        array.append(m)

    run(array)


if __name__ == '__main__':
    initialize_array()
