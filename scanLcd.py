import machine

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0,sda=sda,scl=scl)
print(f"I2C in: {i2c.scan()}")