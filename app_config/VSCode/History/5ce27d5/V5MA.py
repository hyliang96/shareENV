from model import Diffusion_Grad, Diffusion_I2SB, Diffusion_SB, Diffusion_SB_Drift, Diffusion_SB_Beta, Diffusion_SB_VP

decoder_dict = {
    "gradtts": Diffusion_Grad,
    "bridgetts-i2sb": Diffusion_I2SB,
    "bridgetts": Diffusion_SB,
    "bridgetts-beta": Diffusion_SB_Beta,
    "bridgetts-fg": Diffusion_SB_Drift,
    "bridgetts-vp": Diffusion_SB_VP,
}