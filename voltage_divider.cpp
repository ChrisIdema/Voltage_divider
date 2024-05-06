#include <iostream>
#include <cmath>
using namespace std;

/**********************************************
*spanningsdelerderekenaar_2
*(c)2010 Chris Idema
*Dit programma berekend de weerstanden R1 en R2
*van een spanningsdeler. Omdat er bij de meeste
*delers veel mogelijke waarden zijn én er maar
*één de beste kan zijn, is het handig die te
*weten. Dit zelf uitrekenen kost veel werk.
**********************************************/

const int E_12[] = { 100,120,150,180,220,270,
330,390,470,560,680,820 };

const int E_24[] = { 100,110,120,130,150,160,
180,200,220,240,270,300,
330,360,390,430,470,510,
560,620,680,750,820,910 };


double dichtbij(double R1, double verhouding, const int reeks[], int reeksgroote) {
	double R2 = 0;
	double factor = 0.01;//begin bij 1 ohm

						 /*
						 wanneer de gewenste waarde voor R2 groter is dan
						 de eerste waarde van de volgende reeks, schakel
						 dan over naar de volgende reeks.
						 */
	while (((verhouding - 1)*R1)>(double)reeks[0] * 10 * factor) factor *= 10;
	while (((verhouding - 1)*R1)<(double)reeks[reeksgroote - 1] / 10 * factor) factor /= 10;

	for (int i = -1; i <= reeksgroote; i++) {
		if (i<0) {
			R2 = (double)reeks[reeksgroote - 1] / 10 * factor;//laatste waarde vorige reeks als initialisatiewaarde
		}
		else if ((i>-1) && (i<reeksgroote)) {
			//is error bij nieuwe weerstand kleiner dan bij de vorige R2, dan R2 aanpassen
			if (fabs(verhouding*R1 / (R1 + (double)reeks[i] * factor) - 1)<fabs(verhouding*R1 / (R1 + R2) - 1)) R2 = (double)reeks[i] * factor;
		}
		else if (i == reeksgroote) {
			//eerste waarde volgende reeks kan dichterbij zijn dan laatste waarde huidige reeks
			if (fabs(verhouding*R1 / (R1 + (double)reeks[0] * factor * 10) - 1)<fabs(verhouding*R1 / (R1 + R2) - 1)) R2 = (double)reeks[0] * 10 * factor;
		}
	}

	return R2;
}



int main() {
	double dichtbij(double, double, const int[], int);
	cout << "RVDC V2.0 " << char(184) << "2010 Chris Idema" << endl << endl;

	cout << "Ui O-------." << endl;
	cout << "           |" << endl;
	cout << "         .---." << endl;
	cout << "         |   |" << endl;
	cout << "         |R-2|" << endl;
	cout << "         |   |" << endl;
	cout << "         |___|" << endl;
	cout << "           |" << endl;
	cout << "           +-------O Uo" << endl;
	cout << "           |" << endl;
	cout << "         .---." << endl;
	cout << "         |   |" << endl;
	cout << "         |R-1|" << endl;
	cout << "         |   |" << endl;
	cout << "         |___|" << endl;
	cout << "           |" << endl;
	cout << "GND      --+--" << endl;
	cout << "          -+-" << endl;
	cout << "           -" << endl << endl;;

	cout << "Ui: ";
	double Ui;
	cin >> Ui;
	cout << "Uo: ";
	double Uo;
	cin >> Uo;
	/*
	als de uitgang groter is in absolute waarde, of gelijk is aan de ingang,
	dan is er geen spanningsdeler. Is de polariteit van de uitgang ongelijk aan de ingang,
	dan is er geen spanningsdeler. Als de uitgang of de ingang 0 voltia,  zijn er oneindig veel delers mogelijk.
	*/
	if ((fabs(Uo) >= fabs(Ui)) || ((Ui >= 0) != (Uo >= 0)) || (Ui == 0) || (Uo == 0)) {
		cout << "Error! No voltage divider possible with given values.";
	}
	else {
		double verhouding = Ui / Uo;
		double besteR1, besteR2, beste_afwijking = 0;


		cout << endl << "E-24:" << endl;
		for (int i = 0; i<(sizeof(E_24) / sizeof(int)); i++) {
			double R1 = (double)E_24[i] / 100;//begin met 1 ohm
			double R2 = dichtbij(R1, verhouding, E_24, (sizeof(E_24) / sizeof(int)));
			cout << "R1: " << R1 << "ohm" << "\t" << "+ R2: " << R2 << "ohm";
			cout << "\t" << "Uo: " << Ui*R1 / (R1 + R2);
			double afwijking = (Ui*R1 / (R1 + R2) / Uo - 1) * 100;
			cout << "\t" << "error: " << afwijking << "%" << endl;

			if ((fabs(afwijking)<fabs(beste_afwijking)) | (i == 0)) {
				beste_afwijking = afwijking;
				besteR1 = R1;
				besteR2 = R2;
			}

		}
		cout << endl << "-->" << "R1: " << besteR1 << "ohm" << " " << "R2: " << besteR2 << "ohm" << " ";
		cout << "error: " << beste_afwijking << "%" << endl;;

		cout << endl << "E-12:" << endl;
		for (int i = 0; i<(sizeof(E_12) / sizeof(int)); i++) {
			double R1 = (double)E_12[i] / 100;
			double R2 = dichtbij(R1, verhouding, E_12, (sizeof(E_12) / sizeof(int)));
			cout << "R1: " << R1 << "ohm" << "\t" << "+ R2: " << R2 << "ohm";
			cout << "\t" << "Uo: " << Ui*R1 / (R1 + R2);
			double afwijking = (Ui*R1 / (R1 + R2) / Uo - 1) * 100;
			cout << "\t" << "error: " << afwijking << "%" << endl;

			if ((fabs(afwijking)<fabs(beste_afwijking)) | (i == 0)) {
				beste_afwijking = afwijking;
				besteR1 = R1;
				besteR2 = R2;
			}
		}
		cout << endl << "-->" << "R1: " << besteR1 << "ohm" << " " << "R2: " << besteR2 << "ohm" << " ";
		cout << "error: " << beste_afwijking << "%" << endl;;
	}

	cout << endl << endl << "press any key";
	cin.ignore();
	cin.get();

	return 0;
}
