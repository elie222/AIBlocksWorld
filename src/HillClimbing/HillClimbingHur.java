package HillClimbing;

import blocksWorld.BWState;
import blocksWorld.Facts.BWFact;
import aStar.Huristic;

public class HillClimbingHur implements Huristic<BWState> {

	@Override
	public double getHur(BWState node1, BWState node2) {
		int sum = 0;
		for(BWFact f : node2.getFacts())
			if(node1.getFacts().contains(f))
				sum++;
			else sum--;
		return sum;
	}

}
