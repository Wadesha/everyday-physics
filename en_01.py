# -*- coding: utf-8 -*-
"""极少量英文解释：每件器物一段英文简版，事实与中文正文一致。
键为 slug，值为一段英文（不引入中文部分未出现的数字）。"""

EN = {
    "microwave":
        "A microwave oven does not heat food by a water-molecule resonance. At 2.45 GHz the water molecules cannot follow the field at all; the heat comes from dielectric loss, as polar groups are re-oriented against viscous drag on every half cycle and electromagnetic energy becomes thermal energy. Penetration depth in water at 25 C is about 1.4 cm, and one 2.45 GHz photon carries roughly 1e-5 eV, far too little to break a chemical bond. Food heats because it contains polar and ionic species, which is why a dry ceramic plate stays cool.",

    "induction-stove":
        "An induction cooktop rectifies the mains and inverts it to 20 to 40 kHz. The coil sets up an alternating magnetic field, eddy currents are induced in the base of the pot, and the pot itself dissipates heat through ohmic loss, Q = I squared R t. Only the vessel is heated, so the glass surface stays relatively cool and the coupled efficiency reaches 85 to 93 percent, well above a resistive hotplate.",

    "pressure-cooker":
        "Sealing the pot raises the saturated vapour pressure inside, and since saturation pressure rises steeply with temperature the boiling point of water climbs to 112 to 121 C at a gauge pressure of about 0.5 to 1 atmosphere. Collagen and starch break down faster at the higher temperature, which is why cooking time falls to roughly a third. The ceiling is set by the safety valve, and with the pressure released the boiling point drops straight back to 100 C.",

    "thermos":
        "A vacuum flask blocks the three heat paths separately. A vacuum annulus at about 1e-3 Pa removes conduction and convection; a copper or silver coating with an emissivity of 0.02 to 0.05 reflects thermal radiation back; a sealed stopper stops the air circulation that would otherwise carry heat out through the neck. The dominant remaining leak in a good flask is radiation through the coating and conduction along the neck wall.",

    "fridge":
        "A refrigerator and a heat pump are the same machine run in opposite directions: both consume work to move heat from a cold place to a warm one. The coefficient of performance is the heat moved divided by the work consumed, and a domestic refrigerator reaches 2 to 5, while the ideal reverse-Carnot value for 4 C and 25 C is about 13. That is why the condenser coils at the back are hot: the heat delivered to the room is the heat taken from the food plus the work put in.",

    "air-fryer":
        "Air conducts heat about six times worse than cooking oil, so an air fryer compensates with forced convection instead of a better medium. A high-velocity fan raises the convective heat-transfer coefficient until the food surface reaches about 200 C, above the 140 C threshold where Maillard browning starts. The result resembles deep frying because the surface dries and browns, not because hot air conducts like oil.",

    "humidifier":
        "An ultrasonic humidifier drives a piezoelectric disc at 1.7 MHz through the inverse piezoelectric effect. The vibration causes cavitation in the water and tears the surface into droplets of 1 to 5 micrometres, which a small fan carries out as visible mist. The water is never boiled, so dissolved minerals are ejected with the droplets and settle as white dust, a well-known drawback of this design.",

    "static-shock":
        "Walking across a carpet charges an insulated body by triboelectric charging, and the potential can reach 1.5 to 35 kV. Touching a grounded conductor then drives a spark across a millimetre-scale air gap. The stored energy is tiny, because the equivalent capacitance of a human body is only 100 to 250 pF, so the discharge lasts nanoseconds and the current stays in the milliampere range. Dry air and synthetic soles raise the voltage, which is why the effect is worse in winter.",

    "fluorescent-lamp":
        "A low-pressure mercury discharge emits 253.7 nm ultraviolet light, carrying more than 90 percent of the radiated energy, together with a weaker 185.0 nm line. Phosphor on the tube wall absorbs the ultraviolet and re-emits visible light, a two-step conversion that still delivers 25 to 30 percent overall efficiency, roughly four times an incandescent lamp. The excited-state lifetime that governs the mercury lines is 1e-8 to 1e-9 s.",

    "white-led":
        "Electrons and holes recombine across a semiconductor p-n junction and emit photons whose energy is fixed by the band gap: 3.4 eV for GaN, giving blue at 450 to 495 nm. Coating the blue die with a yellow phosphor mixes the two colours into white, at about 300 lm/W and a service life near 100,000 hours. Red needs only 1.4 eV and green 2.26 eV, which is why red and green LEDs existed decades before blue ones.",

    "solar-panel":
        "Photons with more energy than the band gap create electron-hole pairs, and the built-in field of the p-n junction separates them before they can recombine, driving current into an external circuit. Silicon has a gap of 1.1 eV, so much of the solar spectrum is either too low in energy to be absorbed or delivered as surplus heat. The single-junction Shockley-Queisser limit at the optimal gap of 1.34 eV is about 33.7 percent, and the practical ceiling for silicon is 29 to 32 percent.",

    "polarized-sunglasses":
        "Light reflected off water or a wet road at the Brewster angle is almost fully linearly polarized in the horizontal plane. Sunglass lenses have their transmission axis vertical, so Malus law, I = I0 cos squared theta, cuts the horizontal glare while passing about half of the unpolarized background. For a glass surface with index 1.52 the Brewster angle is close to 56.7 degrees.",

    "ar-coating":
        "An anti-reflective coating splits the incoming wave into two reflections, one at the air-film interface and one at the film-glass interface. When the optical thickness is a quarter wavelength the two reflections return out of phase and cancel. A single MgF2 layer of index 1.38 therefore needs a thickness near 99.6 nm for a design wavelength of 550 nm, and the cancellation is only complete at that wavelength, which is why residual colour remains.",

    "optical-fiber":
        "The core carries a slightly higher refractive index than the cladding, 1.4682 against 1.4629. Light arriving at the interface beyond the critical angle undergoes total internal reflection, so the energy stays trapped in the core and bounces forward with very little loss, which is what makes multi-kilometre spans possible. The numerical aperture is about 0.14, giving an acceptance half-angle of roughly 8 degrees at the launch end.",

    "optical-disc":
        "The spiral track of pits and lands on a disc behaves as a reflection grating. Where d sin theta = m lambda, each wavelength reinforces at its own angle, so white light falling on a disc spreads into a spectrum. Track pitch is about 1.6 micrometres on a CD, 0.74 on a DVD and 0.32 on a Blu-ray disc, so the spacing of the colour bands changes with the format, and tilting the surface moves them.",

    "rainbow":
        "Sunlight entering a spherical raindrop, reflecting once inside and leaving again, is concentrated near 42 degrees from the antisolar point, which is the primary bow. Two internal reflections give the secondary bow at about 51 degrees with the colour order reversed and the intensity much weaker. Between the two arcs lies the Alexander dark band, where almost no light is directed, which is why the sky there looks darker than inside either bow. A rainbow is therefore an angular pattern, not an object at a fixed distance.",

    "blue-sky":
        "Air molecules are far smaller than the wavelength of visible light, so they scatter in the Rayleigh regime with an intensity proportional to 1 over lambda to the fourth. Blue is scattered about 4.35 times more strongly than red, which is why the whole sky glows blue rather than the sun looking blue. At sunset the path through the atmosphere is long enough for the short wavelengths to be scattered away, leaving red and orange. Cloud droplets are comparable in size to the wavelength, so they scatter by Mie theory instead and appear white.",

    "green-laser":
        "An 808 nm infrared diode laser pumps a Nd:YVO4 crystal, which lases at 1064 nm. A KTP crystal then doubles the frequency so the wavelength halves to 532 nm and the eye sees green. The green beam is therefore produced by nonlinear frequency conversion inside the pointer rather than by a green-emitting semiconductor, which is why the infrared pump must be filtered out before the beam leaves the housing.",

    "loudspeaker":
        "Audio current flows through a voice coil sitting in a constant magnetic field, and the Lorentz force, F = B l i, drives the coil back and forth. The coil moves the diaphragm, the diaphragm pushes on the air, and the air carries the sound away. Electrical impedance is not flat: at the mechanical resonance of a nominal 8 ohm driver the impedance can rise above 30 ohms, which is why amplifier ratings and enclosure tuning matter.",

    "smoke-detector":
        "A small americium-241 source emits alpha particles of 5.486 MeV that ionize the air in a chamber, sustaining a standing current of about 100 pA. Smoke particles attach to the ions and raise the recombination rate, so the current falls; when it drops past a threshold the alarm trips. The half-life of Am-241 is about 432 years, so the source outlives the detector, and the alpha range in air is only a few centimetres, which is why the sealed foil is not a hazard in normal use.",

    "mri":
        "Hydrogen-1 nuclei have a gyromagnetic ratio of 42.58 MHz/T, so in a 1.5 T scanner they precess at 63.87 MHz and at 3 T at 127.74 MHz. A radio-frequency pulse tips the magnetization, and the signal emitted during relaxation is picked up by coils. Gradient fields make the precession frequency and phase depend on position, so the received signal can be mapped back into an image. There is no ionizing radiation involved; the contrast comes from proton density and relaxation times.",

    "gps":
        "Satellite clocks run 7.2 microseconds per day slow because of special relativity and 45.8 microseconds per day fast because they sit higher in the gravitational potential, giving a net gain of 38.6 microseconds per day. Left uncorrected, that offset would accumulate into a positioning error of about 11 km per day. The correction is built into the transmitted frequency, so a receiver needs no relativistic software of its own.",

    "flash-memory":
        "A flash cell stores charge on a floating gate surrounded by a tunnel oxide about 7 to 10 nm thick. Writing and erasing move electrons through that oxide by Fowler-Nordheim quantum tunnelling, driven by roughly 12 to 20 V, which corresponds to an internal field near 1e9 V/m. The presence or absence of the charge is the stored bit, read out as a shift in threshold voltage. Because the oxide is very thin, repeated cycling eventually damages it, which is the origin of the finite write endurance.",

    "bicycle":
        "A bicycle stays up because leaning automatically steers the front wheel, and that steering brings the wheels back under the centre of mass: a closed feedback loop that needs no rider. Gyroscopic effect and trail are the usual explanations, but neither is necessary. That was shown in Science in April 2011 with a machine whose gyroscopic effect was cancelled by counter-rotating discs and that still self-stabilised above about 8 km/h.",

    "wing-lift":
        "Once the Kutta condition is satisfied the flow leaves the trailing edge smoothly and a circulation is established around the aerofoil. The air accelerates over the upper surface, the pressure there drops, and the lift per unit span follows the Kutta-Joukowski theorem, L = rho V Gamma. The picture holds for subsonic flow below about Mach 0.3, where air behaves as incompressible; at supersonic speed the lift is instead set by the pressure difference across oblique shocks.",

    "typhoon-spin":
        "The Coriolis force arising from the rotation of the Earth deflects moving air to the right in the northern hemisphere and to the left in the southern, so inflowing air spirals into a low-pressure centre anticlockwise north of the equator and clockwise to the south. Within about 5 degrees of the equator the Coriolis force is too weak to organize a vortex, which is why tropical cyclones almost never form there. The 2001 and 2004 systems that came closest left records at about 1.5 and 0.7 degrees of latitude.",
}
