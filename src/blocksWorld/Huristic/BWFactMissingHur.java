package blocksWorld.Huristic;

import blocksWorld.BWState;
import blocksWorld.Facts.BWFact;
import aStar.Huristic;

public class BWFactMissingHur implements Huristic<BWState>{

	@Override
	public double getHur(BWState node1, BWState node2) {
		int distance = 0;
		for(BWFact f : node2.getFacts()){
			if(!node1.getFacts().contains(f))
				distance++;
		}
		return distance;
	}

}
