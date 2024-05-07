import math


def voltage_divider_find_R2(R1, ratio, E):
	R2 = 0
	power = -2 #begin bij 1 ohm

	'''
	wanneer de gewenste waarde voor R2 groter is dan
	de eerste waarde van de volgende reeks, schakel
	dan over naar de volgende reeks.
	'''
	#while (((ratio - 1)*R1)>(double)reeks[0] * 10 * factor) factor *= 10;
	
	while (ratio - 1)*R1 > E[0] * 10 ** (power+1):
		power += 1

	#while (((ratio - 1)*R1)<(double)reeks[reeksgroote - 1] / 10 * factor) factor /= 10;
 
	while (ratio - 1)*R1 < E[-1] * 10 ** (power-1):
		power -= 1


	R2 = E[- 1] * 10 ** (power+0) #laatste waarde vorige reeks als initialisatiewaarde
	for r in E:
		#is error bij nieuwe weerstand kleiner dan bij de vorige R2, dan R2 aanpassen
		if (abs(ratio*R1 / (R1 + r * 10 ** (power+0)) - 1) < abs(ratio*R1 / (R1 + R2) - 1)): 
			R2 = r * 10 ** (power+0)
		

	#eerste waarde volgende reeks kan dichterbij zijn dan laatste waarde huidige reeks
	if (abs(ratio*R1 / (R1 + E[0] * 10 ** (power+1)) - 1) < abs(ratio*R1 / (R1 + R2) - 1)): 
		R2 = E[0] * 10 ** (power+1)
		
	

	return R2




def get_E(m):
	if m <= 24:
		E = [round((10**n)**(1/m)*10)*10 for n in range(0,m)]
	else:
		E = [round((10**n)**(1/m)*100) for n in range(0,m)]

	if m <= 24:
		E = [s+10 if s in (260,290,320,350,380,420,460) else s for s in E]
		E = [s-10 if s in (830,) else s for s in E]

	if m <= 192:
		E = [s+1 if s in (919,) else s for s in E]
	return E



# for m in (12,24,48,96,192):
# 	print(f"E{m}")
# 	E = get_E(m)
# 	print([f"{s/100:.2f}" for s in E])

# def find_series_resistance(R_total, R1, E)



# def find_paralel_resistance(R_total, R1, E):


def find_nearest(R_desired, E):
	#power = (math.log(R_desired, 10)) # not precise, log10(1000)=2.999...
 
	# print(f"R_desired:{R_desired}")

	power = -2 #start at 1 ohm	
	while 100*10 ** (power+1) <= R_desired:
		power += 1
	while 100*10 ** (power) > R_desired:
		power -= 1

	R_nearest = 100*10 ** (power)

	for r in [*E,1000]: #append first value of next range in case value is closer than last value of current range
		if abs(r*10**power - R_desired) < abs(R_nearest-R_desired):
			R_nearest = r*10**power
	
	return R_nearest


# print(find_nearest(0.00099999,get_E(12)))
# print(find_nearest(0.00099999,get_E(12)))
# print(find_nearest(0.001,get_E(12)))
# print(find_nearest(0.0099999,get_E(12)))
# print(find_nearest(0.01,get_E(12)))
# print(find_nearest(0.099999,get_E(12)))
# print(find_nearest(0.1,get_E(12)))
# print(find_nearest(0.90,get_E(12)))
# print(find_nearest(0.91,get_E(12)))
# print(find_nearest(0.92,get_E(12)))
# print(find_nearest(0.99,get_E(12)))
# print(find_nearest(0.999,get_E(12)))
# print(find_nearest(0.999999999,get_E(12)))
# print(find_nearest(1,get_E(12)))
# print(find_nearest(9.999999999,get_E(12)))
# print(find_nearest(10,get_E(12)))
# print(find_nearest(99.999999999,get_E(12)))
# print(find_nearest(100,get_E(12)))
# print(find_nearest(999.999999999,get_E(12)))
# print(find_nearest(1000,get_E(12)))
# print(find_nearest(1001,get_E(12)))

# R_total = 1.93

# print("series circuit:")
# for m in (12, ):
# 	print(f"E{m}:")
# 	E = get_E(m)
# 	best_R2
# 	for R1 in E:



R_total = 1.19
print(f"R_total: {R_total}")

print("parallel circuit:")
for m in (12, ):
	# print(f"E{m}:")
	E = get_E(m)

	best_R1 = None
	best_R2 = None
	best_value = None

	power = -2 #start at 1 ohm	
	while 100*10 ** (power+1) <= R_total:
		power += 1
	while 100*10 ** (power) > R_total:
		power -= 1

	for p in [power,]:
		for r in [*E,1000]:
			R1 = r * 10**p
			if R1 > R_total:
				if best_value == None:
					best_R1 = R1
					ideal_R2 = 1/(1/R_total - 1/R1)
					best_R2 = find_nearest(ideal_R2, E)
					best_value = 1 / (1/best_R1 + 1/best_R2)
				else:
					ideal_R2 = 1/(1/R_total - 1/R1)
					test_R2 = find_nearest(ideal_R2, E)
					test_value = 1 / (1/R1 + 1/test_R2)
					if abs(test_value-R_total) < abs(best_value-R_total):
						best_R1 = R1
						best_R2 = test_R2
						best_value = test_value
	print(f"Best R1//R2: {format(best_R1, '.3g')}//{format(best_R2, '.3g')}=={format(best_value, '.6g')}")

print("series circuit:")
for m in (12, ):
	# print(f"E{m}:")
	E = get_E(m)

	best_R1 = None
	best_R2 = None
	best_value = None

	power = -2 #start at 1 ohm	
	while 100*10 ** (power+1) <= R_total:
		power += 1
	while 100*10 ** (power) > R_total:
		power -= 1

	for p in [power-1,power]:
		for r in E:
			R1 = r * 10**p
			if R1 < R_total and R1 >= R_total/2:
				if best_value == None:
					best_R1 = R1
					ideal_R2 = R_total - R1
					best_R2 = find_nearest(ideal_R2, E)
					best_value = best_R1 + best_R2
				else:
					ideal_R2 = R_total - R1
					test_R2 = find_nearest(ideal_R2, E)
					test_value = R1 + test_R2
					if abs(test_value-R_total) < abs(best_value-R_total):
						best_R1 = R1
						best_R2 = test_R2
						best_value = test_value
	print(f"Best R1+R2: {format(best_R1, '.3g')} + {format(best_R2, '.3g')}=={format(best_value, '.6g')}")




if __name__ == "__main__sdfsdf":

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
		
		first = True
		for m in (12, 24):
			print(f"E{m}:")
			E = get_E(m)
			for r in E:
				R1 = r / 100 #begin met 1 ohm
				R2 = voltage_divider_find_R2(R1, ratio, E)
				afwijking = (Ui*R1 / (R1 + R2) / Uo - 1) * 100
				print(f"R1: {format(R1,'.3g')} ohm\tR2: {format(R2,'.3g')} ohm\tUo: {format(Ui*R1 / (R1 + R2),'.4g')}\terror: {afwijking:5.2f} %")				

				if abs(afwijking) < abs(beste_afwijking) or first:
					beste_afwijking = afwijking
					besteR1 = R1
					besteR2 = R2			
				first = False		
			print(f"-->R1: {format(besteR1,'.3g')} ohm R2: {format(besteR2,'.3g')} ohm error: {beste_afwijking:5.2f} %")
