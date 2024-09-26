from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(
    prefix="/flow",
    tags=["flow"],
)

class Node(BaseModel):
    id: str
    type: str

class Edge(BaseModel):
    source: str
    target: str

class FlowData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class FlowRequest(BaseModel):
    flow_data: FlowData
    initial_input: Any

class FlowResponse(BaseModel):
    result: Any

class ErrorResponse(BaseModel):
    detail: str

def execute_node(node_type, input_data):
    # This function would contain the logic for each node type
    if node_type == 'inputNode':
        return input_data
    elif node_type == 'multiplyNode':
        return input_data * 2
    elif node_type == 'addNode':
        return input_data + 10
    # Add more node types as needed

def process_flow(flow_data, initial_input):
    nodes = {node.id: node for node in flow_data.nodes}
    edges = flow_data.edges
    
    # Create a dictionary to store the output of each node
    node_outputs = {}
    
    # Process nodes in topological order (simplified for this example)
    for node in flow_data.nodes:
        node_id = node.id
        node_type = node.type
        
        # Find input edges for this node
        input_edges = [edge for edge in edges if edge.target == node_id]
        
        if not input_edges:
            # This is an input node
            node_outputs[node_id] = execute_node(node_type, initial_input)
        else:
            # Get the output from the source node of the first input edge
            input_data = node_outputs[input_edges[0].source]
            node_outputs[node_id] = execute_node(node_type, input_data)
    
    # Return the output of the last node (assuming it's the output node)
    return node_outputs[flow_data.nodes[-1].id]

@router.post("/process", response_model=FlowResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def process_flow_endpoint(flow_request: FlowRequest):
    """
    Process a flow and return the result.

    Example:
    ```
    curl -X 'POST' \
      'http://localhost:8000/flow/process' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "flow_data": {
        "nodes": [
          {"id": "1", "type": "inputNode"},
          {"id": "2", "type": "multiplyNode"},
          {"id": "3", "type": "addNode"}
        ],
        "edges": [
          {"source": "1", "target": "2"},
          {"source": "2", "target": "3"}
        ]
      },
      "initial_input": 5
    }'
    ```
    """
    try:
        flow_data = flow_request.flow_data
        initial_input = flow_request.initial_input
        
        if not flow_data or initial_input is None:
            raise HTTPException(status_code=400, detail="Invalid input data")
        
        result = process_flow(flow_data, initial_input)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
