import pandas as pd
import matplotlib.pyplot as plt

# 1. importul unei fișier csv sau json în pachetul pandas;
df=pd.read_csv("Travel_details.csv")
print(df)

#2. metode specifice unei liste
#creare lista de nume - metoda list
list_nume=list(df["Traveler_name"])
print(list_nume)

# Crearea unei liste cu informațiile despre călătorie.
# Vizualizarea listei cu informații despre călătorie
lista_calatorie = []
for index, row in df.iterrows():
    calatorie = [row['Trip_ID'],row['Destination'], row['Start_date'], row['End_date'],row['Accommodation_type'], row['Accommodation_cost']]
    lista_calatorie.append(calatorie)

for calatorie in lista_calatorie:
    print(calatorie)

#adaugare element in lista - append
list_nume.append("Alina Elena")
print(list_nume[-1])

#adaugarea pe poz 0 , metoda insert
list_nume.insert(0,"Bogdan Andreea")
print(list_nume[0])

# #eliminarea unui element - remove
list_nume.remove("Bogdan Andreea")
print('Aici a fost sters Bogdan Andreea si la aceasta pozitie este '+list_nume[0])
#metoda len
print(len(list_nume))

# #copy
lista_copie=list_nume.copy()
print(lista_copie)

#del pt a sterge el de la indexul specificat
del lista_copie[1]
print(lista_copie)

#clear
lista_copie.clear()
print(lista_copie)

# #index
list_nume.index("John Smith")

# # 3. utilizarea structurilor repetitive;
list_transport_cost=list(df["Transportation_cost"])
print(list_transport_cost)

n=len(list_transport_cost)
i=0
while i< n:
    if list_transport_cost[i]<=1000:
        list_transport_cost[i]= list_transport_cost[i]-100
    i=i+1
print(list_transport_cost)

# # 4. definirea și apelarea unor funcții;

def filtreaza_dupa_nationalitate(data, nationalitate):
    filtrat = data[data['Traveler_nationality'] == nationalitate]
    return filtrat

# Apelarea funcției
nationalitate = 'British'
calatorii_filtrate = filtreaza_dupa_nationalitate(df, nationalitate)
print("Călătoriile cu naționalitatea", nationalitate, "sunt:")
print(calatorii_filtrate)



def numara_valori_maxime(data):
    max_value = data["Transportation_cost"].max()
    numar_maxime = data[data["Transportation_cost"] == max_value].shape[0]
    inregistrari_maxime = data[data["Transportation_cost"] == max_value]
    return numar_maxime, inregistrari_maxime

numar_maxime, inregistrari_maxime = numara_valori_maxime(df)
print("\nNumarul de valori maxime din tabela de cost de transport:", numar_maxime)
print("Inregistrările cu valorile maxime de cost de transport:")
print(inregistrari_maxime)


def gaseste_destinatie_cautata(data):
    destinatii_cautate = data['Destination'].value_counts()
    cea_mai_cautata_destinatie = destinatii_cautate.idxmax()
    return cea_mai_cautata_destinatie

destinatie_cautata = gaseste_destinatie_cautata(df)
print("Cea mai cautata destinatie este:", destinatie_cautata)

def tipuri_ieftine_cazare(data):
    tipuri_cazare = data['Accommodation_type'].unique()
    cost_minim = 999999
    tipuri_ieftine = []

    for tip in tipuri_cazare:
        cost_tip_cazare = data[data['Accommodation_type'] == tip]['Accommodation_cost'].min()
        if cost_tip_cazare < cost_minim:
            cost_minim = cost_tip_cazare
            tipuri_ieftine = [tip]
        elif cost_tip_cazare == cost_minim:
            tipuri_ieftine.append(tip)
    return tipuri_ieftine

tipuri_ieftine_cazare =tipuri_ieftine_cazare(df)
print("Cele mai ieftine tipuri de cazare sunt:", tipuri_ieftine_cazare)


# 5. tratarea valorilor lipsă din Transportation_cost
print(df['Transportation_cost'])
values = df['Transportation_cost'].mean()
df['Transportation_cost'] = df['Transportation_cost'].fillna(value = values)
print(df['Transportation_cost'])

# 6. accesarea datelor cu loc si iloc
#loc
# Afișarea turistilor care au avut o vacanta de 7 zile si aveau sexul feminin
tabel=(df.loc[(df['Duration_days']==7)&(df['Traveler_gender']=='Female'),['Traveler_name','Destination','Traveler_age','Traveler_gender','Traveler_nationality']])
print('Afișarea turistilor care au avut o vacanta de 7 zile si aveau sexul feminin',tabel)
print(tabel['Traveler_name'].count())
# # iloc - afiseaza inregistrarile cu info despre clatori
traveler=df.iloc[:,[5,6,7,8]]
print(traveler)

# 7. prelucrarea seturilor de date cu merge / join;

tipuri_ieftine = df.groupby(['Destination', 'Accommodation_type'])['Accommodation_cost'].min().reset_index()
tipuri_ieftine = tipuri_ieftine.sort_values('Accommodation_cost').head(len(tipuri_ieftine) // 2)
tabel_ieftine_cazare = tipuri_ieftine.merge(df[['Destination', 'Accommodation_type', 'Accommodation_cost', 'Trip_ID']],
                                         on=['Destination', 'Accommodation_type', 'Accommodation_cost'], how='left')

print('Cele mai ieftine tipuri de cazare\n',tabel_ieftine_cazare)

result=pd.merge(traveler,
                df[["Destination","Traveler_name"]],
                on="Traveler_name",
                how='left')
print('Informatiile despre calatori si destinatia aleasa:\n',result)


# # 8. utilizarea funcțiilor de grup;
 # in functie de destinatie si durata calatoriei sa vedem cate persoane au ales acea destinatie si durata minima si maxima

df1=df.groupby(['Destination','Duration_days']).agg({ 'Destination':"count",
                                                     'Duration_days':[min,max]})
print(df1)

# # In functie de numele calatorului, cate zile a calatorit
df2=df.groupby('Traveler_name')['Duration_days'].sum()
print(df2)

# # 9.- # modificarea datelor în pachetul pandas
# # # daca tipul de transport este Train sa se modifice costul in plus cu 200.
print(df[df['Transportation_type']=='Train'])
df.loc[df['Transportation_type']=='Train',"Transportation_cost"] = df["Transportation_cost"]+200
print(df[df['Transportation_type']=='Train'])

# # 10. reprezentare grafică a datelor cu pachetul matplotlib; pentru transport cost
pd.set_option("display.max_columns",10)
print(df['Transportation_cost'])
df['Transportation_cost'].plot(kind='hist')
plt.xlabel('Transportation_cost')
plt.show()


# Crearea graficului de tip pie
tipuri_cazare = df['Accommodation_type'].value_counts()
labels = tipuri_cazare.index
sizes = tipuri_cazare.values
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # Asigurarea unei forme circulare pentru grafic
plt.title('Distribuția tipurilor de cazare')

plt.show()

print('stergeri\n')
# # 11. ștergerea de coloane și înregistrări;
# #Sterge o coloana cu axis = 1 ----------
df = df.drop("Trip_ID", axis=1) #axis=1-col #axis=0-linii
print(df)
# #Sterge o coloana cu parametrul columns
df = df.drop(columns="Accommodation_cost")
print(df)
# stergere inregistrari ----------------
# Sterge tipul de transport train
df = df.set_index("Transportation_type")
df = df.drop("Train", axis=0)
df.to_csv("Train_empty.csv")



