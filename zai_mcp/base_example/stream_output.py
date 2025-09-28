# Stream output example for MCP
# This file demonstrates streaming output functionality

import time
import threading
from typing import Generator, Any
from queue import Queue, Empty

class StreamOutput:
    """Base class for streaming output functionality"""
    
    def __init__(self):
        self.output_queue = Queue()
        self.is_streaming = False
        self.stream_thread = None
    
    def generate_stream(self, content: str, chunk_size: int = 10) -> Generator[str, None, None]:
        """Generate content in chunks for streaming"""
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
            time.sleep(0.1)  # Simulate processing time
    
    def start_streaming(self, content: str):
        """Start streaming content in a separate thread"""
        if self.is_streaming:
            return
        
        self.is_streaming = True
        
        def _stream_content():
            for chunk in self.generate_stream(content):
                if not self.is_streaming:
                    break
                self.output_queue.put(chunk)
            self.output_queue.put(None)  # End of stream marker
        
        self.stream_thread = threading.Thread(target=_stream_content)
        self.stream_thread.start()
    
    def get_next_chunk(self, timeout: float = 1.0) -> str:
        """Get the next chunk from the stream"""
        try:
            chunk = self.output_queue.get(timeout=timeout)
            if chunk is None:  # End of stream
                self.is_streaming = False
                return ""
            return chunk
        except Empty:
            return ""
    
    def stop_streaming(self):
        """Stop the streaming process"""
        self.is_streaming = False
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=1.0)

class RealTimeStreamer(StreamOutput):
    """Real-time streaming with callback support"""
    
    def __init__(self):
        super().__init__()
        self.callbacks = []
    
    def add_callback(self, callback):
        """Add a callback function to be called with each chunk"""
        self.callbacks.append(callback)
    
    def start_streaming_with_callbacks(self, content: str):
        """Start streaming with callback support"""
        if self.is_streaming:
            return
        
        self.is_streaming = True
        
        def _stream_with_callbacks():
            for chunk in self.generate_stream(content):
                if not self.is_streaming:
                    break
                
                # Put in queue
                self.output_queue.put(chunk)
                
                # Call all registered callbacks
                for callback in self.callbacks:
                    try:
                        callback(chunk)
                    except Exception as e:
                        print(f"Callback error: {e}")
            
            self.output_queue.put(None)
        
        self.stream_thread = threading.Thread(target=_stream_with_callbacks)
        self.stream_thread.start()

class BatchStreamProcessor:
    """Process multiple streams in batches"""
    
    def __init__(self, max_concurrent_streams: int = 5):
        self.max_concurrent_streams = max_concurrent_streams
        self.active_streams = []
    
    def process_multiple_streams(self, contents: list) -> list:
        """Process multiple content streams"""
        results = []
        
        for i in range(0, len(contents), self.max_concurrent_streams):
            batch = contents[i:i + self.max_concurrent_streams]
            batch_results = self._process_batch(batch)
            results.extend(batch_results)
        
        return results
    
    def _process_batch(self, batch: list) -> list:
        """Process a batch of streams"""
        streamers = []
        
        # Start all streams in the batch
        for content in batch:
            streamer = StreamOutput()
            streamer.start_streaming(content)
            streamers.append(streamer)
        
        # Collect results
        batch_results = []
        while streamers:
            for streamer in streamers[:]:
                chunk = streamer.get_next_chunk(timeout=0.1)
                if chunk:
                    if not hasattr(streamer, 'collected_content'):
                        streamer.collected_content = ""
                    streamer.collected_content += chunk
                elif not streamer.is_streaming:
                    # Stream finished
                    batch_results.append(getattr(streamer, 'collected_content', ""))
                    streamers.remove(streamer)
        
        return batch_results

if __name__ == "__main__":
    # Example usage
    streamer = StreamOutput()
    test_content = "This is a test content that will be streamed in chunks."
    
    print("Starting stream...")
    streamer.start_streaming(test_content)
    
    full_content = ""
    while True:
        chunk = streamer.get_next_chunk()
        if chunk:
            print(f"Received chunk: {chunk}")
            full_content += chunk
        else:
            break
    
    print(f"\nFull content: {full_content}")
    
    # Real-time streamer example
    realtime_streamer = RealTimeStreamer()
    
    def print_callback(chunk):
        print(f"Callback: {chunk}")
    
    realtime_streamer.add_callback(print_callback)
    realtime_streamer.start_streaming_with_callbacks("Real-time streaming test.")
    
    time.sleep(2)  # Let it stream for a bit
    realtime_streamer.stop_streaming()