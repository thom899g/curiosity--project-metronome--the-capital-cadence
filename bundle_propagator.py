import aiohttp
import asyncio
from typing import Dict, List

class BundlePropagator:
    def __init__(self, relay_urls: List[str]):
        self.relays = relay_urls
        
    async def _submit_to_relay(self, relay_url: str, bundle: Dict) -> bool:
        """Submit a single bundle to a relay and return success status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(relay_url, json=bundle) as response:
                    if response.status == 200:
                        return True
                    else:
                        print(f"Relay {relay_url} returned status {response.status}")
                        return False
        except Exception as e:
            print(f"Error submitting to relay {relay_url}: {e}")
            return False
        
    async def propagate_bundle(self, bundle: Dict) -> bool:
        """Submit bundle to multiple relays, first success wins"""
        tasks = []
        for relay in self.relays:
            task = self._submit_to_relay(relay, bundle)
            tasks.append(task)
        
        # Race submissions
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return any(r is True for r in results)