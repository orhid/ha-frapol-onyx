import asyncio
import logging

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)


class FrapolHub:
    """Handle Modbus communication with Frapol Onyx."""

    def __init__(
        self,
        host: str,
        port: int,
        slave: int,
        timeout: int,
        retries: int,
    ) -> None:
        self.slave = slave
        self._lock = asyncio.Lock()

        self.client = AsyncModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout,
            retries=retries,
        )

    async def async_connect(self) -> None:
        """Connect to the Modbus gateway."""
        async with self._lock:
            if not await self.client.connect():
                raise ConnectionError("Unable to connect to Frapol gateway")

    async def async_close(self) -> None:
        """Close the connection."""
        async with self._lock:
            self.client.close()

    async def async_read_register(self, address: int) -> int:
        """Read one holding register."""
        async with self._lock:
            if not self.client.connected and not await self.client.connect():
                raise ConnectionError("Modbus connection unavailable")

            result = await self.client.read_holding_registers(
                address=address,
                count=1,
                device_id=self.slave,
            )

            if result.isError():
                raise ModbusException(f"Error reading register {address}: {result}")

            return result.registers[0]

    async def async_write_register(
        self,
        address: int,
        value: int,
    ) -> None:
        """Write one holding register."""
        async with self._lock:
            if not self.client.connected and not await self.client.connect():
                raise ConnectionError("Modbus connection unavailable")

            result = await self.client.write_register(
                address=address,
                value=value,
                device_id=self.slave,
            )

            if result.isError():
                raise ModbusException(f"Error writing register {address}: {result}")
