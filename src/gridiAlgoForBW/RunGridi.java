package gridiAlgoForBW;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import blocksWorld.BWState;
import blocksWorld.Box;
import blocksWorld.Actions.BWAction;
import blocksWorld.Actions.BWPickUpAction;
import blocksWorld.Actions.BWPutOnAction;
import blocksWorld.Actions.BWPutOnTableAction;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWFreeFact;
import blocksWorld.Facts.BWOnFact;
import blocksWorld.Facts.BWOnTableFact;

public class RunGridi {
	
	BWState fin;
	BWState cur;
	public final List<BWState> path = new ArrayList<BWState>();
	
	public RunGridi(BWState fin){
		this.fin = fin;
	}
	
	public List<BWState> run(BWState init){
		cur = init;
		path.add(cur);
		for(BWFact f : fin.getFacts())
			if(f instanceof BWOnTableFact){
				putOnTable(f.getBoxes()[0]);
				//System.out.println("on table");
				build(f.getBoxes()[0]);
			}
		return path;
	}

	private void build(Box box) {
		Box above = findAbove(box, BWAction.getRelatedFacts(fin, box));
		if(above == null)
			makeFree(box);
		else {
			putOn(above,box);
			build(above);
		}
	}

	private void putOn(Box above, Box box) {
		Collection<BWFact> relatedFacts = BWAction.getRelatedFacts(cur, box);
		if(relatedFacts.contains(new BWOnFact(above,box)))
			return;
		makeFree(above);
		makeFree(box);
		doAction(new BWPickUpAction(above));
		doAction(new BWPutOnAction(box));
	}

	private void makeFree(Box box) {
		Collection<BWFact> relatedFacts = BWAction.getRelatedFacts(cur, box);
		if(relatedFacts.contains(new BWFreeFact(box)))
			return;
		else{
			Box above = findAbove(box,relatedFacts);
			makeFree(above);
			doAction(new BWPickUpAction(above));
			doAction(new BWPutOnTableAction(above));		
		}
	}

	private void putOnTable(Box box) {
		Collection<BWFact> relatedFacts = BWAction.getRelatedFacts(cur, box);
		if(relatedFacts.contains(new BWOnTableFact(box)))
			return;
		makeFree(box);
		doAction(new BWPickUpAction(box));
		doAction(new BWPutOnTableAction(box));
	}
	
	private Box findAbove(Box box, Collection<BWFact> relatedFacts) {
		for(BWFact f : relatedFacts){
			if(f instanceof BWOnFact && f.getBoxes()[1].equals(box))
				return f.getBoxes()[0];
			if(f.equals(new BWFreeFact(box)))
				return null;
		}
		return null; // should not reach hear
	}

	private void doAction(BWAction ac){
		cur = ac.perform(cur);
		path.add(cur);
	}
}
