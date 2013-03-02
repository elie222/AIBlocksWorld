package blocksWorld.Huristic;

import blocksWorld.BWState;
import aStar.Huristic;

public class TestHuristic implements Huristic<BWState> {

	/*
	 * check if astar working
	 * (non-Javadoc)
	 * @see aStar.Huristic#getHur(aStar.Node)
	 */
	@Override
	public double getHur(BWState node1,BWState node2) {
		return 0;
	}
	
}
