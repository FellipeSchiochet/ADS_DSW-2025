try:
    idade = int(input("informe seu idade: \n\n"))
    print(f"Sua idade daqui a 10 anos será: {idade + 10}")
except ValueError:
    print("Erro: Favor digitar um número! 🥵")
