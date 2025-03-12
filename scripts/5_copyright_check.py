def make_transformative(clip):
    return clip.fx(vfx.colorx, 0.8)\
        .fx(vfx.lum_contrast, lum=0.8)\
        .fx(vfx.rotate, lambda t: 0.5*np.sin(t/3))\
        .speedx(1.2)
