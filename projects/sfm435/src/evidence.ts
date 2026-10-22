// Producer-verified rendered Java from the tested projections at one pinned commit.
// Ellipsis comments below are editorial omission markers, not source lines.
export const revision='8e349578d18511d8d5993b66a3ad3c7c957e5db4';
export const inputExcerpt=`@Override
public void tick(ProgramContext context) {
    context.addInput(this);
    // … rest of method omitted …
}`;
export const baselineExcerpt=`if (resourceType.isEmpty(extracted)) {
    // … comment and logging omitted …
    source.setDone();
    return;
}`;
export const fixedExcerpt=`if (resourceType.isEmpty(extracted)) {
    // … comments and logging omitted …
    return;
}`;
export const extractionExcerpt=`// extract item for real
STACK extracted = source.extract(amountAvailableToMove);`;
export const insertionExcerpt=`// insert item for real
STACK extractedRemainder = destination.insert(extracted, false);

// track transfer amounts
var moved = resourceType.getAmountDifference(extracted, extractedRemainder);
source.tracker.trackTransfer(resourceType, extracted, moved);
destination.tracker.trackTransfer(resourceType, extracted, moved);`;
export const sourceLabel='Rendered Java • 8e349578 • … = omitted source';
