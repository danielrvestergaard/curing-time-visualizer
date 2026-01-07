import numpy as np

class Concrete2004:
    '''
    Concrete with properties as per EN 1992-1-1:2004.

    '''

    F_CK_DICT = {'C12/15': 12.0, 'C16/20': 16.0, 'C20/25': 20.0,
                 'C25/30': 25.0, 'C30/37': 30.0, 'C35/45': 35.0,
                 'C40/50': 40.0, 'C45/55': 45.0, 'C50/60': 50.0,
                 'C55/67': 55.0, 'C60/75': 60.0, 'C70/85': 70.0,
                 'C80/95': 80.0, 'C90/105': 90.0, }

    S_DICT = {'S': 0.38, 'N': 0.25, 'R': 0.20}

    def __init__(self, strength_class: str, cement_class: str,
                 curing_temperature: float=20.0):

        self.strength_class = strength_class
        self.cement_class = cement_class
        self.curing_temperature = curing_temperature

    @property
    def f_ck(self) -> float:
        ''' Characteristic compressive strength [MPa] '''
        return self.F_CK_DICT[self.strength_class]

    @property
    def f_cm(self) -> float:
        ''' Mean compressive strength [MPa] '''
        return self.get_fcm(self.f_ck)

    @property
    def E_cm(self) -> float:
        ''' Secant modulus of elasticity [MPa] '''
        return self.get_Ecm(self.f_ck)

    @property
    def s(self) -> float:
        ''' Strength development coefficient '''
        return self.get_s(self.cement_class)

    @staticmethod
    def get_fcm(f_ck: float) -> float:
        '''
        Calculates the mean compressive strength cf. Table 3.1.

        Parameters:
            f_ck (float): Characteristic compressive strength [MPa]
        Returns:
            f_cm (float): Mean compressive strength [MPa]

        '''
        return f_ck+8.0  # [MPa]

    @staticmethod
    def get_Ecm(f_cm: float) -> float:
        '''
        Calculates the approximate indicative value for the modulus
        of elasticity cf. Table 3.1. (secant modulus for stresses
        between 0 and 0.4*f_cm)

        Parameters:
            f_cm (float): Mean compressive strength [MPa]
        Returns:
            E_cm (float): Modulus of elasticity [MPa]
        '''
        return 22e3*(f_cm/10)**0.3

    @staticmethod
    def get_fcm_t(beta_cc_t: float, f_cm: float) -> float:
        '''
        Calculates the age-adjusted mean compressive strength cf.
        3.1.2(6), Eq. 3.1.

        Parameters:
            beta_cc_t (float): Age-adjustment coefficient
            f_cm (float): Mean compressive strength at t=28 days [MPa]
        Returns:
            f_cm_t (float): Age-adjusted mean compressive strength [MPa]

        '''
        return beta_cc_t*f_cm

    @staticmethod
    def get_Ecm_t(beta_cc_t: float, E_cm: float) -> float:
        '''
        Calculates the age-adjusted modulus of elasticity cf. 3.1.3(3),
        eq. 3.5.

        Parameters:
            beta_cc_t (float): Age-adjustment coefficient
            E_cm (float): Modulus of elasticity at t=28 days [MPa]
        Returns:
            E_cm_t (float): Age-adjusted modulus of elasticity [MPa]

        '''
        return beta_cc_t**(0.3)*E_cm

    @staticmethod
    def get_fck_t(f_cm_t: float) -> float:
        '''
        Calculates the age-adjusted characteristic compressive strength
        cf. 3.1.2(5).

        Parameters:
            f_cm_t (float): Age-adjusted mean compressive strength [MPa]
        Returns:
            f_ck_t (float): Age-adjusted characteristic compressive
                strength [MPa]

        '''
        return f_cm_t-8.0

    @staticmethod
    def get_betacc_t(s: float, t: float) -> float:
        '''
        Calculates the age-adjustment coefficient cf. 3.1.2(6), Eq. 3.2.

        Parameters:
            s (float): Coefficient dependent on the cement type
            t (float): The concrete age [days]
        Returns:
            beta_cc_t (float): Age-adjustment coefficient
        '''
        t = minimum(t, 28.0)
        return exp(s*(1.0-(28.0/t)**0.5))

    def get_t_T(dt: np.ndarray, T_dt: np.ndarray,
                use_linear_activation_energy: bool=True):
        '''
        Calculates the temperature-adjusted age cf. B.1(3), Eq. B.10

        Parameters:
            dt (NDArray): Time periods [days]
            T_dt (NDArray): Temperatures in time periods [degree C]
            use_linear_activation_energy (bool): Use the linear,
                temperature-dependent expression for the activation
                energy cf. SBI125instead of the constant value in
                DS/EN 1992-1-1:2004? This is conservative (default:
                True)
        Returns:
            t_T (float): Temperature-adjusted age [days]
        '''
        if min(T_dt) <= 0.0 or max(T_dt) > 80.0:
            raise Exception('The temperature should be between 0 and 80 '
                            'degrees C')

        R = 8.314  # Gas constant [J/mol C]
        E = 33500.0  # Activation energy [J/mol]
        if use_linear_activation_energy:
            E += 1470*np.maximum(20.0-T, 0.0)

        return sum(dt*np.exp(E/R*(1.0/293.0-1.0/(273.0+T_dt))))

    @staticmethod
    def get_s(cement_class: str) -> float:
        '''
        Calculates the coefficient s which depends on the type of
        cement cf. 3.1.2(6).

        Parameters:
            cement_class (str): The cement class
        Returns:
            s (float): Coefficient that depends on the type of cement

        '''
        return self.S_C_DICT[cement_class]

class Concrete2023:
    '''
    Concrete with properties as per EN 1992-1-1:2023.

    Modifiable attributes:
        strength_class (str)
        strength_development_class (str)
        t_ref (float)
        t (float)
        curing_temperature (float)
    Read-only attributes:
        f_ck (float)
        f_cm (float)
        E_cm (float)
        s_C (float)
        beta_cc_t (float)
        f_cm_t (float)
        E_cm_t (float)
        f_ck_t (float)
    Methods:
        get_fcm(f_ck)
        get_Ecm(f_cm, k_E=9_500.0)
        get_fcm_t(beta_cc_t, f_cm)
        get_Ecm_t(beta_cc_t, E_cm)
        get_fck_t(f_cm_t)
        get_betacc_t(s_C, t, t_ref=28.0)
        get_t_T(t, T, use_linear_activation_energy=True)
        get_sC(f_ck, strength_development_class)

    '''

    F_CK_DICT = {'C12/15': 12.0, 'C16/20': 16.0, 'C20/25': 20.0,
                 'C25/30': 25.0, 'C30/37': 30.0, 'C35/45': 35.0,
                 'C40/50': 40.0, 'C45/55': 45.0, 'C50/60': 50.0,
                 'C55/67': 55.0, 'C60/75': 60.0, 'C70/85': 70.0,
                 'C80/95': 80.0, 'C90/105': 90.0, 'C100/115': 100.0}

    S_C_DICT = {'CS': [0.6, 0.5, 0.4],
                'CN': [0.5, 0.4, 0.3],
                'CR': [0.3, 0.2, 0.1]}

    def __init__(self, strength_class: str, strength_development_class: str,
                 t_ref: float=28.0, age: float=28.0,
                 curing_temperature: float=20.0):

        self.strength_class = strength_class
        self.strength_development_class = strength_development_class
        self.t_ref = t_ref
        self.age = age
        self.curing_temperature = curing_temperature

    #region PROPERTIES

    @property
    def f_ck(self) -> float:
        ''' Characteristic compressive strength [MPa] '''
        return self.F_CK_DICT[self.strength_class]

    @property
    def f_cm(self) -> float:
        ''' Mean compressive strength [MPa] '''
        return self.get_fcm(self.f_ck)

    @property
    def E_cm(self) -> float:
        ''' Secant modulus of elasticity [MPa] '''
        return self.get_Ecm(self.f_ck)

    @property
    def s_C(self) -> float:
        ''' Strength development coefficient '''
        return self.get_sC(self.f_ck, self.strength_development_class)

    @property
    def beta_cc_t(self) -> float:
        ''' Age-adjustment coefficient beta_cc(t) '''
        return self.get_betacc_t(self.s_C, self.t_T, self.t_ref)

    @property
    def f_cm_t(self) -> float:
        ''' Age-adjusted mean compressive strength [MPa] '''
        return self.get_fcm_t(self.beta_cc_t, self.f_cm)

    @property
    def E_cm_t(self) -> float:
        ''' Age-adjusted modulus of elasticity [MPa] '''
        return self.get_Ecm_t(self.beta_cc_t, self.E_cm)

    @property
    def f_ck_t(self) -> float:
        ''' Age-adjusted characteristic compressive strength [MPa] '''
        return self.get_fck_t(self.f_cm_t)

    @property
    def t_T(self) -> float:
        ''' Temperature-adjusted age [days] '''
        return self.get_t_T(self.age, self.curing_temperature)

    #endregion

    #region METHODS

    @staticmethod
    def get_fcm(f_ck: float) -> float:
        '''
        Calculates the mean compressive strength cf. 5.1.3(3)

        Parameters:
            f_ck (float): Characteristic compressive strength [MPa]
        Returns:
            f_cm (float): Mean compressive strength [MPa]

        '''
        return f_ck+8.0  # [MPa]

    @staticmethod
    def get_Ecm(f_cm: float, k_E: float=9_500.0) -> float:
        '''
        Approximate indicative value for the modulus of elasticity cf.
        5.1.4(2) (secant modulus for stresses between 0 and 0.4*f_cm)

        Parameters:
            f_cm (float): Mean compressive strength [MPa]
            k_E (float): Coefficient dependent on the aggregate type.
                Can vary between 5000 and 13000 (default: 9500 corre-
                sponding to quartzite aggregates)
        Returns:
            E_cm (float): Modulus of elasticity [MPa]
        '''
        return k_E*f_cm**(1/3)

    @staticmethod
    def get_fcm_t(beta_cc_t: float, f_cm: float) -> float:
        '''
        Calculates the age-adjusted mean compressive strength cf.
        B.4(1), Eq. B.1.

        Parameters:
            beta_cc_t (float): Age-adjustment coefficient
            f_cm (float): Mean compressive strength at t=t_ref [MPa]
        Returns:
            f_cm_t (float): Age-adjusted mean compressive strength [MPa]

        '''
        return beta_cc_t*f_cm

    @staticmethod
    def get_Ecm_t(beta_cc_t: float, E_cm: float) -> float:
        '''
        Calculates the age-adjusted modulus of elasticity cf. B.4(4),
        eq. B.4.

        Parameters:
            beta_cc_t (float): Age-adjustment coefficient
            E_cm (float): Modulus of elasticity at t=t_ref [MPa]
        Returns:
            E_cm_t (float): Age-adjusted modulus of elasticity [MPa]

        '''
        return beta_cc_t**(1/3)*E_cm

    @staticmethod
    def get_fck_t(f_cm_t: float) -> float:
        '''
        Calculates the age-adjusted characteristic compressive strength.
        NOTE: This is not explicitly covered in DS/EN 1992-1-1:2023!

        Parameters:
            f_cm_t (float): Age-adjusted mean compressive strength [MPa]
        Returns:
            f_ck_t (float): Age-adjusted characteristic compressive
                strength [MPa]

        '''
        return f_cm_t-8.0

    @staticmethod
    def get_betacc_t(s_C: float, t: float, t_ref: float=28.0) -> float:
        '''
        Calculates the age-adjustment coefficient cf. B.4(1), Eq. B.2.

        Parameters:
            s_C (float): Coefficient dependent on  early strength
                development of the concrete and the concrete strength
            t (float): The concrete age [days]
            t_ref (float): The time at which f_ck is determined [days];
                may be taken between 28 and 91 days when specified for
                a project, or 28 days in general (default: 28.0)
        Returns:
            beta_cc_t (float): Age-adjustment coefficient
        '''
        t = np.minimum(t, t_ref)
        return np.exp(s_C*(1.0-np.sqrt(t_ref/t))*np.sqrt(28.0/t_ref))

    @staticmethod
    def get_t_T(t: float, T: float, use_linear_activation_energy: bool=True):
        '''
        Calculates the temperature-adjusted age cf. B.5(5), Eq. B.18,
        for at constant temperature.

        Parameters:
            t (float): Concrete age [days]
            T (float): Temperatures in curing period [degree C]
            use_linear_activation_energy (bool): Use the linear,
                temperature-dependent expression for the activation
                energy cf. SBI125instead of the constant value in
                DS/EN 1992-1-1:2023? This is conservative (default:
                True)
        Returns:
            t_T (float): Temperature-adjusted age [days]
        '''
        if not (0.0 < T <= 80.0):
            raise Exception('The temperature should be between 0 and 80 '
                            'degrees C')

        R = 8.314  # Gas constant [J/mol C]
        E = 33500.0  # Activation energy [J/mol]
        if use_linear_activation_energy:
            E += 1470*np.maximum(20.0-T, 0.0)

        return t*np.exp(E/R*(1.0/293.0-1.0/(273.0+T)))

    @classmethod
    def get_sC(cls, f_ck: float, strength_development_class: str) -> float:
        '''
        Calculates the coefficient s_C which depends on the early
        strength development of the concrete and the concrete strength
        cf. B.4(1), Table B.2.

        Parameters:
            f_ck (float): Characteristic compressive strength (at t_ref)
            cement_class (str): The cement class (see B.3(1))
        Returns:
            s_C (float): Coefficient that depends on the early strength
                development of the concrete and the concrete strength

        '''
        if f_ck <= 35.0:
            return cls.S_C_DICT[strength_development_class][0]
        elif f_ck < 60.0:
            return cls.S_C_DICT[strength_development_class][1]
        else:
            return cls.S_C_DICT[strength_development_class][2]

    #endregion
