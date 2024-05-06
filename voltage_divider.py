E_12 = (100,120,150,180,220,270,330,390,470,560,680,820)

E_24 = (100,110,120,130,150,160,
180,200,220,240,270,300,
330,360,390,430,470,510,
560,620,680,750,820,910)


def find_R2(R1, ratio, series):
	R2 = 0
	power = -2 #begin bij 1 ohm

	'''
	wanneer de gewenste waarde voor R2 groter is dan
	de eerste waarde van de volgende reeks, schakel
	dan over naar de volgende reeks.
	'''
	#while (((ratio - 1)*R1)>(double)reeks[0] * 10 * factor) factor *= 10;
	
	while (ratio - 1)*R1 > series[0] * 10 ** (power+1):
		power += 1

	#while (((ratio - 1)*R1)<(double)reeks[reeksgroote - 1] / 10 * factor) factor /= 10;
 
	while (ratio - 1)*R1 < series[-1] * 10 ** (power-1):
		power -= 1


	R2 = series[- 1] * 10 ** (power+0) #laatste waarde vorige reeks als initialisatiewaarde
	for r in series:
		#is error bij nieuwe weerstand kleiner dan bij de vorige R2, dan R2 aanpassen
		if (abs(ratio*R1 / (R1 + r * 10 ** (power+0)) - 1) < abs(ratio*R1 / (R1 + R2) - 1)): 
			R2 = r * 10 ** (power+0)
		

	#eerste waarde volgende reeks kan dichterbij zijn dan laatste waarde huidige reeks
	if (abs(ratio*R1 / (R1 + series[0] * 10 ** (power+1)) - 1) < abs(ratio*R1 / (R1 + R2) - 1)): 
		R2 = series[0] * 10 ** (power+1)
		
	

	return R2



if __name__ == "__main__":

	ascii_art = '''RVDC V2.0 ©2024 Chris Idema
Ui O-------.
           |
         .---.
         |   |
         |R-2|
         |   |
         |___|
           |
           +-------O Uo
           |
         .---.
         |   |
         |R-1|
         |   |
         |___|
           |
GND      --+--
          -+-
           -
'''
	print(ascii_art)

	#print(find_R2(1, 5.0/3.3, E_12))
 
	Ui = 5.0
	Uo = 3.3

	print(f"Ui: {Ui}")
	print(f"Uo: {Uo}")


	'''
	als de uitgang groter is in absolute waarde, of gelijk is aan de ingang,
	dan is er geen spanningsdeler. Is de polariteit van de uitgang ongelijk aan de ingang,
	dan is er geen spanningsdeler. Als de uitgang of de ingang 0 voltia,  zijn er oneindig veel delers mogelijk.
	'''
	if ((abs(Uo) >= abs(Ui)) or ((Ui >= 0) != (Uo >= 0)) or (Ui == 0) or (Uo == 0)):
		print("Error! No voltage divider possible with given values.")
	
	else:
		ratio = Ui / Uo
		besteR1 = 0
		besteR2 = 0
		beste_afwijking = 0

		print("E-24:")
		first = True
		for r in E_24:
			R1 = r / 100 #begin met 1 ohm
			R2 = find_R2(R1, ratio, E_24)
			afwijking = (Ui*R1 / (R1 + R2) / Uo - 1) * 100
			print(f"R1: {R1} ohm\tR2: {R2:3f} ohm\tUo: {Ui*R1 / (R1 + R2):4f}\terror: {afwijking:5.2f} %")

			if abs(afwijking) < abs(beste_afwijking) or first:
				beste_afwijking = afwijking
				besteR1 = R1
				besteR2 = R2			
			first = False

		
		print(f"-->R1: {besteR1} ohm R2: {besteR2} ohm error: {beste_afwijking:5.2f} %")

		print("E-12:")
		first = True
		for r in E_12:
			R1 = r / 100 #begin met 1 ohm
			R2 = find_R2(R1, ratio, E_12)
			afwijking = (Ui*R1 / (R1 + R2) / Uo - 1) * 100
			print(f"R1: {R1} ohm\tR2: {R2:2f} ohm\tUo: {Ui*R1 / (R1 + R2):4f}\terror: {afwijking:5.2f} %")

			if abs(afwijking) < abs(beste_afwijking) or first:
				beste_afwijking = afwijking
				besteR1 = R1
				besteR2 = R2			
			first = False

		print(f"-->R1: {besteR1} ohm R2: {besteR2} ohm error: {beste_afwijking:5.2f} %")