package aStar;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.PriorityQueue;

public class RunAstar<N extends Node<N>> {
	
	private N _goal;
	private long nodeMaxExpanded = -1;
	
	public RunAstar(N goal){
		this._goal = goal;
	}
	
	public Results Search(N start, Huristic<N> hur){
		long nodesExpanded = 0;
		ArrayList<ExtandedNode> visited = new ArrayList<ExtandedNode>();
		PriorityQueue<ExtandedNode> unvisited = new PriorityQueue<ExtandedNode>();
		unvisited.add(new ExtandedNode(start,0,hur.getHur(start,_goal)));
		ExtandedNode goal = null;
		ExtandedNode reachHear = null;
		while(!unvisited.isEmpty()){
			ExtandedNode temp = unvisited.poll();
			visited.add(temp);
			//System.out.println("\n-----------------interation---------------\n");
			//System.out.println(temp);
			//System.out.println("\n-----------------interation----------------\n");
			if(_goal.equals(temp.getNode())){
				goal = temp;
				break;
			}
			
			nodesExpanded++;
			if(nodesExpanded > nodeMaxExpanded && nodeMaxExpanded != -1){
				reachHear = temp;
				break;
			}
			
			for(N child : temp.getChildren()){
				
				ExtandedNode childNode = new ExtandedNode(child,temp.getDist() + child.getDistFromParent(),hur.getHur(child,_goal),temp);
				
				boolean visit = false;
				for(ExtandedNode n : visited)
					if(n.equals(childNode))
						if(n.getDist()<=childNode.getDist())
						{
							visit = true;
							break;
						}
				
				if(visit)
					continue;
				
				boolean unvisit = false;
				for(ExtandedNode n : unvisited)
					if(n.equals(childNode))
						if(n.getDist()<=childNode.getDist())
						{
							unvisit = true;
							break;
						}
				
				if(unvisit)
					continue;
				
				while(unvisited.remove(childNode));
				while(visited.remove(childNode));

				unvisited.add(childNode);
			}
			
		}
		
		if(goal==null){
			//System.out.println("path didnot found");
			LinkedList<N> path = new LinkedList<N>();
			
			ExtandedNode tmp = reachHear;
			while(tmp!=null){
				path.addFirst(tmp.getNode());
				tmp = tmp.getParent();
			}

			return new Results(path,-1);
		}
		else{
			LinkedList<N> path = new LinkedList<N>();
			
			ExtandedNode tmp = goal;
			while(tmp!=null){
				path.addFirst(tmp.getNode());
				tmp = tmp.getParent();
			}

			return new Results(path,nodesExpanded);
		}
	}
	
	
	public void setNodeMaxExpanded(long nodeMaxExpanded) {
		this.nodeMaxExpanded = nodeMaxExpanded;
	}

	public long getNodeMaxExpanded() {
		return nodeMaxExpanded;
	}


	public class Results{
		public final long nodesExpended;
		public final List<N> path;
		
		public Results(List<N> path, long ne){
			this.path = path;
			this.nodesExpended = ne;
		}
		
		public long size(){
			return path==null?-1:path.size();
		}
	}
	
	public class ExtandedNode implements Comparable<ExtandedNode>{

		N node;
		ExtandedNode parent;
		double dist;
		double hur;
		
		public ExtandedNode(N node, double dist, double hur){
			this.node = node;
			this.dist = dist;
			this.hur = hur;
		}
		
		public ExtandedNode getParent() {
			return parent;
		}

		public ExtandedNode(N node, double dist, double hur, ExtandedNode parent){
			this.node = node;
			this.dist = dist;
			this.hur = hur;
			this.parent = parent;
		}
		
		public double getDist(){
			return dist;
		}
		
		public Collection<N> getChildren() {
			return (Collection<N>) node.getChildren();
		}

		public N getNode() {
			return node;
		}

		@Override
		public int compareTo(ExtandedNode o) {
			if(dist + hur > o.dist + o.hur)
				return 1;
			if(dist + hur < o.dist + o.hur)
				return -1;
			return 0;
		}
		
		public boolean equals(Object o){
			return node.equals(((ExtandedNode)o).node);
		}
		
		public String toString(){
			return node.toString();
		}
		
	}
}
