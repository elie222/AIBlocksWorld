package blocksWorld;

import java.util.Collection;
import java.util.Iterator;
import blocksWorld.Actions.*;
import blocksWorld.Facts.BWFact;
import blocksWorld.Facts.BWOnFact;
import blocksWorld.Facts.BWOnTableFact;

public class GetResults {
	 
	public static String getResults(Collection<BWState> res){
		String result = "";
		BWState cur,prev;
		Iterator<BWState> i = res.iterator();
		if(!i.hasNext())
			return null;
		prev = i.next();
		if(!i.hasNext())
			return null;
		
		cur = i.next();
		for(; i.hasNext() ; prev = cur,cur = i.next()){
			if(!cur.isArmEmpty())
				result += "pick up " + cur.getHoldByArm().toString() + "\n";
			else
				result += "put " + prev.getHoldByArm().toString() + " on " + findOn(cur,prev.getHoldByArm()) + "\n";
		}
		if(!cur.isArmEmpty())
			result += "pick up " + cur.getHoldByArm().toString() + "\n";
		else
			result += "put " + prev.getHoldByArm().toString() + " on " + findOn(cur,prev.getHoldByArm()) + "\n";
		return result;
	}

	private static String findOn(BWState cur, Box holdByArm) {
		Collection<BWFact> facts = BWAction.getRelatedFacts(cur,holdByArm);
		for(BWFact f : facts){
			if(f instanceof BWOnTableFact)
				return "Table";
			if(f instanceof BWOnFact)
				return f.getBoxes()[1].toString();
		}
		return null;
	}
	
}
