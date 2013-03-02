package blocksWorld.Huristic;

import java.util.Collection;

import blocksWorld.BWState;
import blocksWorld.Actions.BWAction;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;
import blocksWorld.Facts.BWOnFact;
import blocksWorld.Facts.BWOnTableFact;
import aStar.Huristic;

public class BWFactDistHur implements Huristic<BWState>{

	@Override
	public double getHur(BWState node1, BWState node2) {
		int distance = 0;
		for(BWFact f : node2.getFacts()){
			if(node1.getFacts().contains(f))
				continue;
			if(f instanceof BWFreeFact)
				continue;
			if(f instanceof BWOnTableFact){
				Collection<BWFact> t = BWAction.getRelatedFacts(node1,f.getBoxes()[0]);
				if(t.isEmpty()){
					distance++;
					continue;
				}
				//if(t.contains(new BWFreeFact(f.getBoxes()[0])))
				distance+=2;
				//else distance+=4;
			}
			if(f instanceof BWOnFact){
				Collection<BWFact> t = BWAction.getRelatedFacts(node1,f.getBoxes()[0]);
				Collection<BWFact> t1 = BWAction.getRelatedFacts(node1,f.getBoxes()[1]);
				if(t.isEmpty()){
					if(t1.contains(new BWFreeFact(f.getBoxes()[1])))
						distance++;
					else distance+=3;
					continue;
				}
				if(t1.isEmpty()){
					//if(t.contains(new BWFreeFact(f.getBoxes()[0])))
						distance+=3;
					//else distance+=5;
					continue;
				}
				//if(t.contains(new BWFreeFact(f.getBoxes()[0])))
				distance+=2;
				//else distance+=4;
				//if(!t1.contains(new BWFreeFact(f.getBoxes()[1])))
					//distance+=2;
			}
		}
		//System.out.println("hur = " + distance);
		return distance;
	}

}
