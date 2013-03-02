package blocksWorld.Huristic;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import blocksWorld.BWProbCreator;
import blocksWorld.Box;
import blocksWorld.BWState;
import blocksWorld.GetResults;
import blocksWorld.Actions.BWAction;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWOnFact;
import aStar.Huristic;
import aStar.RunAstar;
import blocksWorld.BWProb;

public class BWLearningHur implements Huristic<BWState> {
	
	@Override
	public double getHur(BWState node1, BWState node2) {
		BWState cur = node1.dup();
		BWState fin = node2.dup();
		Collection<BWFact> r = new ArrayList<BWFact>();
		boolean isChange = false;
		for(BWFact f : cur.getFacts())
			for(BWFact f1 : fin.getFacts()){
				if(f.equals(f1) && f instanceof BWOnFact){
					Collection<BWFact> d = BWAction.getRelatedFacts(cur, f.getBoxes()[0]);
					for(BWFact a : d){
						if(a.equals(f1))
							continue;
						if(a instanceof BWOnFact)
							a.getBoxes()[1].setName(f.getBoxes()[1].toString());
						else a.getBoxes()[0].setName(f.getBoxes()[1].toString());
					}
					d = BWAction.getRelatedFacts(fin, f.getBoxes()[0]);
					for(BWFact a : d){
						if(a.equals(f1))
							continue;
						if(a instanceof BWOnFact)
							a.getBoxes()[1].setName(f.getBoxes()[1].toString());
						else a.getBoxes()[0].setName(f.getBoxes()[1].toString());
					}
					f.getBoxes()[0].setName(f.getBoxes()[1].toString());
					f1.getBoxes()[0].setName(f1.getBoxes()[1].toString());
					r.add(new BWOnFact(f.getBoxes()[1],f.getBoxes()[1]));
					isChange = true;
				}
			}
		for(BWFact e : r){
			cur.getFacts().remove(e);
			fin.getFacts().remove(e);
		}
		//System.out.println(cur);
		//System.out.println("---------------------");
		//System.out.println(fin);
		if(!isChange)
			return (new BWFactDistHur()).getHur(node1, node2);
		else{
			RunAstar<BWState> a = new RunAstar<BWState>(fin);
			a.setNodeMaxExpanded(30);
			RunAstar<BWState>.Results w = a.Search(cur, new BWFactDistHur());
			//probs.add(new BWProb(cur,fin,w.path.size()));
			int ttt = 0;
			for(BWFact e : r)
				if(GetResults.getResults(w.path) != null){
					//System.out.println(GetResults.getResults(w.path));
					String[] s = GetResults.getResults(w.path).split("pick up " + e.getBoxes()[0]);
					if(s != null)
						ttt += s.length-1;
			}
			return Math.max(w.path.size() + ttt*4,(new BWFactDistHur()).getHur(node1, node2));
		}
	}
}
