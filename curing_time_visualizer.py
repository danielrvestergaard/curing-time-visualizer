from ipywidgets import widgets
from matplotlib import pyplot as plt
import numpy as np

from concrete import Concrete2004, Concrete2023

class CuringTimeVisualizer:

    X_TICKS = np.arange(0, 28+1, 2)

    def __init__(self, concrete_class: type):
        self.concrete = concrete_class(
            self.default_strength_class,
            self.default_strength_development_class,
            age=self.default_age,
            curing_temperature = self.default_curing_temperature
        )

    @property
    def default_strength_class(self) -> str:
        return 'C30/37'

    @property
    def default_strength_development_class(self) -> str:
        return 'CN'

    @property
    def default_age(self) -> float:
        return 28.0

    @property
    def default_curing_temperature(self) -> float:
        return 20.0

    def plot_curves(self, strength_class: str, strength_development_class: str,
                    t: float, T: float):


        # Generate age plotting data
        # - Find age corresponding to t_T = 3 days (for which f_ck is valid)
        t_T_min = 3.0
        t_min = t_T_min*np.exp(4000/(273+T)-13.65)
        # - Generate data on each side of t_T = 3 days
        dt = 28/100  # Sample spacing
        n_samples = [int(t_min//dt+1), int((28.0-t_min)//dt+1)]
        t_list = np.hstack((
            np.linspace(0.01, t_min, n_samples[0]),
            np.linspace(t_min, 28.0, n_samples[1]),
        ))
        # - Get index of t_T = 3 days
        idx = np.argmax(t<=t_list)

        # Assign values to concrete attributes
        self.concrete.strength_class = strength_class
        self.concrete.strength_development_class = strength_development_class
        self.concrete.age = t_list
        self.concrete.curing_temperature = T


        # Generate plot
        #fig, axs = self.fig, self.axs
        fig, axs = plt.subplots(
            ncols=2, figsize=(8, 4), constrained_layout=True
        )

        # Apply x-axis formatting
        for ax in axs:
            ax.set_xlim(0, 28)
            ax.set_xticks(self.X_TICKS)
            ax.set_xlabel('Concrete age: $t$ [days]')
            #ax.clear()   # Clear the existing plot

        # Set titles
        axs[0].set_title('Strength')
        axs[1].set_title('Stiffness')

        # Apply y-axis formatting
        axs[0].set_ylim(0, self.concrete.f_ck)
        axs[0].set_ylabel(r'Compressive strength: $f_\mathrm{ck}(t)$ [MPa]')
        axs[0].set_yticks(np.arange(0, self.concrete.f_ck+1, 5))
        axs[1].set_ylim(0, np.ceil((1e-3*self.concrete.E_cm)/5)*5)
        axs[1].set_ylabel(r'Modulus of elasticity: $E_\mathrm{cm}(t)$ [GPa]')
        #axs[1].set_yticks(np.arange(0, self.concrete.E_cm+1, 5))

        # Add curves to plot
        E_cm_t, f_ck_t = self.concrete.E_cm_t, self.concrete.f_ck_t
        axs[0].plot([0, t_list[idx], t_list[idx]],
                    [f_ck_t[idx], f_ck_t[idx], 0],
                    '-', color=[0.8, 0.8, 0.8])
        axs[0].plot(t_list[:n_samples[0]], f_ck_t[:n_samples[0]], ':b')
        axs[0].plot(t_list[n_samples[0]:], f_ck_t[n_samples[0]:], '-b')
        axs[0].plot(t_list[idx], f_ck_t[idx], '.b', markersize=10)

        axs[1].plot([0, t_list[idx], t_list[idx]],
                    [1e-3*E_cm_t[idx], 1e-3*E_cm_t[idx], 0],
                    '-', color=[0.8, 0.8, 0.8])
        axs[1].plot(t_list[:n_samples[0]], 1e-3*E_cm_t[:n_samples[0]], ':r')
        axs[1].plot(t_list[n_samples[0]:], 1e-3*E_cm_t[n_samples[0]:], '-r')
        axs[1].plot(t_list[idx], 1e-3*E_cm_t[idx], '.r', markersize=10)

        #plt.draw()   # Update the plot whenever this function is executed

    def display(self):
        heading = widgets.HTML(
            '<h1>Concrete curing time visualizer</h1>'
        )
        explanation = widgets.HTML(
            '<p>Explore the interdependencies between curing temperature, curing time, and the compressive strength and stiffness of concrete according to EN 1992-1-1:2023.</p>'
        )
        display(heading)
        display(explanation)
        w = widgets.interact(
            self.plot_curves,
            strength_class=self._strength_dropdown,
            strength_development_class=self._strength_development_dropdown,
            T=self._T_slider,
            t=self._t_slider,
        )

    @property
    def _T_slider(self) -> widgets.IntSlider:
        ''' The temperature slider '''
        slider = widgets.IntSlider(
            value=20,
            min=5,
            max=20,
            step=1,
            description='Temperature [\u00b0C]:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            style={'description_width': 'initial'}
        )

        return slider

    @property
    def _t_slider(self) -> widgets.IntSlider:
        ''' The concrete age slider '''
        slider = widgets.IntSlider(
            value=28,
            min=0,
            max=28,
            step=1,
            description=r'Concrete age [days]:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            style={'description_width': 'initial'}
        )

        return slider

    @property
    def _strength_dropdown(self) -> widgets.Dropdown:
        strength_classes = list(self.concrete.F_CK_DICT.keys())
        dropdown = widgets.Dropdown(
            options=strength_classes,
            value=strength_classes[4],
            description='Strength class:',
            disabled=False,
            style={'description_width': 'initial'}
        )

        return dropdown

    @property
    def _strength_development_dropdown(self) -> widgets.Dropdown:
        strength_development_classes = list(self.concrete.S_C_DICT.keys())
        dropdown = widgets.Dropdown(
            options=strength_development_classes,
            value=strength_development_classes[1],
            description='Strength development class:',
            disabled=False,
            style={'description_width': 'initial'}
        )

        return dropdown
