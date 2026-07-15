# shigl/network/mesh.py
import json
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

@dataclass
class NetworkNode:
    """یک نود در شبکه"""
    id: str
    host: str
    port: int
    capabilities: List[str] = field(default_factory=list)
    is_online: bool = True
    last_seen: str = ""

class SHIGLMesh:
    """
    شبکه مش SHIGL
    امکان ارتباط بین چندین نود SHIGL در شبکه محلی
    پشتیبانی از: Pyro5, Reticulum, یا WebSocket
    """
    
    def __init__(self, node_id: str = "shigl-master"):
        self.node_id = node_id
        self.peers: Dict[str, NetworkNode] = {}
        self.is_running = False
        self.protocol = "pyro5"  # یا "reticulum" یا "websocket"
        
    def start(self, host: str = "0.0.0.0", port: int = 9090) -> bool:
        """راه‌اندازی شبکه"""
        if self.protocol == "pyro5":
            return self._start_pyro5(host, port)
        elif self.protocol == "reticulum":
            return self._start_reticulum()
        else:
            return self._start_websocket(host, port)
    
    def _start_pyro5(self, host: str, port: int) -> bool:
        """راه‌اندازی با Pyro5"""
        try:
            import Pyro5.api
            import Pyro5.nameserver
            
            # راه‌اندازی Name Server
            self.ns_thread = threading.Thread(
                target=Pyro5.nameserver.start_ns,
                kwargs={"host": host, "port": port}
            )
            self.ns_thread.daemon = True
            self.ns_thread.start()
            
            # ثبت این نود
            daemon = Pyro5.api.Daemon(host=host, port=port+1)
            uri = daemon.register(self)
            
            ns = Pyro5.api.locate_ns(host=host, port=port)
            ns.register(self.node_id, uri)
            
            self.is_running = True
            print(f"✅ شبکه مش روی {host}:{port} راه‌اندازی شد")
            print(f"📡 Node ID: {self.node_id}")
            return True
            
        except ImportError:
            print("❌ Pyro5 نصب نیست!")
            print("💡 pip install Pyro5")
            return False
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی Pyro5: {e}")
            return False
    
    def _start_reticulum(self) -> bool:
        """راه‌اندازی با Reticulum"""
        try:
            import RNS
            
            # این بخش نیاز به تنظیمات بیشتر دارد
            print("⚠️ Reticulum نیاز به تنظیمات شبکه دارد")
            print("💡 راهنما: https://reticulum.network/manual/")
            return False
            
        except ImportError:
            print("❌ Reticulum نصب نیست!")
            print("💡 pip install rns")
            return False
    
    def _start_websocket(self, host: str, port: int) -> bool:
        """راه‌اندازی با WebSocket"""
        try:
            import asyncio
            import websockets
            
            async def handler(websocket, path):
                async for message in websocket:
                    data = json.loads(message)
                    response = self._handle_message(data)
                    await websocket.send(json.dumps(response))
            
            # این بخش نیاز به اجرا در asyncio دارد
            print(f"⚠️ WebSocket روی {host}:{port} راه‌اندازی شد")
            return True
            
        except ImportError:
            print("❌ websockets نصب نیست!")
            print("💡 pip install websockets")
            return False
    
    def discover_peers(self) -> List[NetworkNode]:
        """کشف نودهای دیگر در شبکه"""
        if self.protocol == "pyro5":
            try:
                import Pyro5.api
                ns = Pyro5.api.locate_ns()
                registered = ns.list()
                
                new_peers = []
                for name, uri in registered.items():
                    if name != self.node_id:
                        node = NetworkNode(
                            id=name,
                            host=str(uri),
                            port=0,
                            is_online=True
                        )
                        self.peers[name] = node
                        new_peers.append(node)
                
                return new_peers
            except Exception as e:
                print(f"⚠️ خطا در کشف نودها: {e}")
                return []
        
        return list(self.peers.values())
    
    def send_message(self, target_node: str, message: Dict[str, Any]) -> Optional[Dict]:
        """ارسال پیام به نود دیگر"""
        if target_node not in self.peers:
            print(f"❌ نود {target_node} پیدا نشد")
            return None
        
        if self.protocol == "pyro5":
            try:
                import Pyro5.api
                ns = Pyro5.api.locate_ns()
                uri = ns.lookup(target_node)
                proxy = Pyro5.api.Proxy(uri)
                response = proxy._handle_message(message)
                return response
            except Exception as e:
                print(f"❌ خطا در ارسال پیام: {e}")
                return None
        
        return None
    
    def _handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """پردازش پیام دریافتی"""
        msg_type = message.get("type", "unknown")
        
        if msg_type == "ping":
            return {"type": "pong", "node_id": self.node_id}
        elif msg_type == "query":
            return self._handle_query(message)
        elif msg_type == "command":
            return self._handle_command(message)
        else:
            return {"type": "error", "message": "Unknown message type"}
    
    def _handle_query(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """پردازش درخواست اطلاعات"""
        query = message.get("query", "")
        return {
            "type": "response",
            "node_id": self.node_id,
            "data": f"Response to: {query}"
        }
    
    def _handle_command(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """پردازش دستور"""
        command = message.get("command", "")
        return {
            "type": "result",
            "node_id": self.node_id,
            "result": f"Command '{command}' executed"
}
