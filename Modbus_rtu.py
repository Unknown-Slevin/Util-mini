from sys import byteorder


def create_modbus_rtu_packet(slave_address, function, data_area, starting_address, quantity_of_data, values=None):
    """
    Формирует пакет Modbus RTU, автоматически выбирая код функции.  Поддерживает больше функций.

    Args:
        slave_address: Адрес слейва (1 байт).
        function: 'read' или 'write' (строка).
        data_area: 'coil', 'input', 'holding', 'input_register' (строка).
        starting_address: Начальный адрес (целое число).
        quantity_of_data: Количество данных (целое число).
        values: Список значений для записи (только для функций записи).

    Returns:
        Байтовый массив, представляющий пакет Modbus RTU, или None в случае ошибки.
    """
    try:
        # Проверка входных данных
        if not (0 < slave_address < 256):
            raise ValueError("Некорректный адрес слейва.")
        if function not in ('read', 'write'):
            raise ValueError("Некорректная функция ('read' или 'write').")
        if data_area not in ('coil', 'input', 'holding', 'input_register'):
            raise ValueError("Некорректная область памяти ('coil', 'input', 'holding' или 'input_register').")
        if not (0 <= starting_address):
            raise ValueError("Некорректный начальный адрес.")
        if not (0 < quantity_of_data):
            raise ValueError("Некорректное количество данных.")
        if function == 'write' and (values is None or len(values) < quantity_of_data ):
            raise ValueError("Для функций записи необходимо указать значения.")


        # Выбор кода функции
        if function == 'read':
            if data_area == 'coil':
                function_code = 0x01  # Read Coils
            elif data_area == 'input':
                function_code = 0x02  # Read Input Status
            elif data_area == 'holding':
                function_code = 0x03  # Read Holding Registers
            elif data_area == 'input_register':
                function_code = 0x04  # Read Input Registers
            else:
                raise ValueError("Неподдерживаемая область памяти для чтения.")
        elif function == 'write':
            if data_area == 'coil':
                if quantity_of_data == 1:
                    function_code = 0x05  # Force Single Coil
                else:
                    function_code = 0x0F  # Force Multiple Coils
            elif data_area == 'holding':
                if quantity_of_data == 1:
                    function_code = 0x06  # Preset Single Register
                else:
                    function_code = 0x10  # Preset Multiple Registers
            else:
                raise ValueError("Неподдерживаемая область памяти для записи.")
        else:
            raise ValueError("Неизвестная функция.")


        # Формирование пакета
        data = [slave_address, function_code]
        if function == 'read':
            if data_area in ('holding', 'input_register'):
                data.extend(starting_address.to_bytes(2, byteorder='big'))
                data.extend(quantity_of_data.to_bytes(2, byteorder='big'))
            else:
                data.extend(starting_address.to_bytes(2, byteorder='big'))
                data.extend((quantity_of_data // 8 + (quantity_of_data % 8 > 0)).to_bytes(2, byteorder='big'))
        elif function == 'write':
            if function_code == 0x05 or function_code == 0x06:  # Single Coil/Register
                    data.extend(starting_address.to_bytes(2, byteorder='big'))
                    data.extend(values[0].to_bytes(1 if function_code == 0x05 else 2, byteorder='big'))
            elif function_code == 0x0F:  # Multiple Coils
                data.extend(starting_address.to_bytes(2, byteorder='big'))
                data.extend(quantity_of_data.to_bytes(2, byteorder='big'))
                byte_count = (quantity_of_data + 7) // 8
                data.extend(byte_count.to_bytes(1, byteorder='big'))
                byte_array = bytearray((len(values) + 7) // 8)
                for i in range(0, quantity_of_data):
                    if values[i]:
                        byte_array[i // 8] |= (1 << (i % 8))
                data.extend(byte_array)
            elif function_code == 0x10:  # Multiple Registers
                data.extend(starting_address.to_bytes(2, byteorder='big'))
                data.extend(quantity_of_data.to_bytes(2, byteorder='big'))
                byte_count = quantity_of_data * 2
                data.extend(byte_count.to_bytes(1, byteorder='big'))
                for i in range(quantity_of_data):
                    data.extend(values[i].to_bytes(2, byteorder='big'))

        crc = calculate_crc16(data)
        data.extend(crc.to_bytes(2, byteorder='big'))

        return bytes(data)

    except ValueError as e:
        print(f"Ошибка при формировании пакета Modbus RTU: {e}")
        return None

    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return None





def calculate_crc16(data):
    """Вычисляет CRC16 для данных Modbus RTU."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return (crc >> 8) | ((crc & 0xFF) << 8)
