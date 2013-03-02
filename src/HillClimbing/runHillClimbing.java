
package HillClimbing;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Random;

import aStar.Huristic;
import aStar.Node;

public class runHillClimbing<N extends Node<N>> {
	
	private N _goal;
	private N _start;
	public static double propebility = 1;
	public static int SerachTill = 20;
	public static int tryAgain = 50;
	public static int s = -1;
	
	public runHillClimbing(N goal){
		this._goal = goal;
	}
	
	public Collection<N> Search(N start, Huristic<N> hur){
		double interation = 0;
		int trys = 0;
		_start = start;
		Collection<N> path = new ArrayList<N>();
		path.add(start);
		int see = 0;
		while(!start.equals(_goal)){
			if(see == SerachTill){
				see = 0;
				start = _start;
				path = new ArrayList<N>();
				path.add(start);
				propebility = 1;
				if(trys >= tryAgain){
					trys = 0;
					SerachTill+=1;
					s -= 1;
					interation = 0;
					//tryAgain--;
					//interation++;
					//propebility = 1 - Math.pow(1 - 1/interation, interation);//thank you halutzi
					//propebility = 1 - Math.pow(1/interation, interation);
				}else trys++;
			}
			Collection<N> child = start.getChildren();
			N bestChild = null;
			double best = 0;
			double temp1 = 0;
			for(N temp : child){
				if((temp1 = hur.getHur(temp, _goal)) > best && !temp.equals(start)){
					best = temp1;
					bestChild = temp;
				}
			}
			Random r = new Random();
			N temp2 = null;
			if(r.nextDouble() < propebility)
				do{
					temp2 = (N) child.toArray()[r.nextInt(child.size())];
				}while(start.equals(temp2));
			else temp2 = bestChild;
			if(!temp2.equals(start)){
				path.add(temp2);
				see++;
			}
			start = temp2;
			interation++;
			propebility = 1/Math.pow(interation, 1/s);
		}
		return path;
	}
}
