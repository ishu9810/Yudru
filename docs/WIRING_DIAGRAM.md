# Wiring Diagram (Text)

For each drone:
- FC UART2 TX -> USB-UART RX
- FC UART2 RX -> USB-UART TX
- FC GND -> USB-UART GND
- FC 5V -> adapter 5V (if needed by adapter)

Use 5-port powered USB hub to Windows GCS.
